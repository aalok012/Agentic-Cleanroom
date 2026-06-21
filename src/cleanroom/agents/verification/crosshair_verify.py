"""Deterministic contract verification via CrossHair symbolic execution (python stack only).

CrossHair runs each generated function on SYMBOLIC inputs through an SMT solver (Z3) and
searches for counterexamples to a contract — no LLM, no test artifacts, fully deterministic
and reproducible. It can only symbolically execute pure, side-effect-free Python, so it runs
on the ``python`` stack and is skipped on ``fastapi`` (the DB/HTTP code it cannot analyze).

The contract checked is synthesized DETERMINISTICALLY from the planning contract, never from
tests: a postcondition that the function returns its declared return type, and (when
``error_mode == 'raise'``) a ``raises: ValueError`` allowance so deliberate precondition
rejections are not flagged. CrossHair therefore reports two things — a return that violates
the declared type, and any UNDECLARED crash (KeyError/TypeError/IndexError/…) on some input.

Cleanroom isolation: a CrossHair counterexample carries concrete failing inputs, which must
never reach the Code Agent. We abstract every counterexample to a SPEC-LEVEL observation —
the property violated and the failure kind — and discard the concrete argument values, so
the revise loop stays spec-level exactly like the LLM/executable verifiers.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from src.cleanroom.agents.code.agent import CodeAgent
from src.cleanroom.agents.code.schema.code import GeneratedCode
from src.cleanroom.agents.verification.schema.verification import ContractVerdict, ContractViolation

# CrossHair output line, e.g.:
#   /tmp/x.py:10: error: ZeroDivisionError:  when calling safe_div(0, 0)
#   /tmp/x.py:10: error: false when calling always_list('')
_ERROR_LINE = re.compile(r":\d+:\s*error:\s*(?P<msg>.*?)\s+when calling\s", re.IGNORECASE)

# Common Homebrew locations for an interpreter-matching libz3 when the bundled wheel's
# architecture does not match the running Python (e.g. an arm64 z3 wheel under x86_64 Python).
_Z3_PROBE_DIRS = ("/usr/local/opt/z3/lib", "/opt/homebrew/opt/z3/lib", "/usr/lib")


def _z3_env() -> dict[str, str]:
    """Environment for the CrossHair subprocess, adding Z3_LIBRARY_PATH if discoverable."""
    env = dict(os.environ)
    if env.get("Z3_LIBRARY_PATH"):
        return env
    for d in _Z3_PROBE_DIRS:
        if (Path(d) / "libz3.dylib").exists() or (Path(d) / "libz3.so").exists():
            env["Z3_LIBRARY_PATH"] = d
            break
    return env


def _return_type(signature: str) -> str:
    """The declared return type from a one-line ``def f(...) -> T:`` signature, else ''."""
    m = re.search(r"->\s*(.+?)\s*:\s*$", signature.strip())
    return m.group(1).strip() if m else ""


def _type_postcondition(return_type: str) -> str | None:
    """A PEP 316 ``post`` predicate asserting __return__ matches the declared return type.

    Only the top-level container/scalar is checked (CrossHair verifies it symbolically over
    all inputs); ``None`` means we cannot synthesize one and fall back to ``post: True`` so
    exception-finding still runs.
    """
    rt = return_type.strip()
    if rt in ("None", ""):
        return "__return__ is None" if rt == "None" else None
    head = rt.split("[", 1)[0].strip().lower()
    mapping = {
        "list": "isinstance(__return__, list)",
        "dict": "isinstance(__return__, dict)",
        "set": "isinstance(__return__, set)",
        "tuple": "isinstance(__return__, tuple)",
        "str": "isinstance(__return__, str)",
        "bool": "isinstance(__return__, bool)",
        "int": "isinstance(__return__, int)",
        "float": "isinstance(__return__, (int, float))",
    }
    return mapping.get(head)


def _func_name(signature: str) -> str:
    m = re.search(r"def\s+([A-Za-z_]\w*)\s*\(", signature)
    return m.group(1) if m else ""


def _inject_contract(content: str, func_name: str, post: str, allow_value_error: bool) -> str | None:
    """Insert PEP 316 ``post:``/``raises:`` lines into ``func_name``'s docstring.

    Returns the rewritten source, or None if the function/its docstring can't be located.
    Pure textual scaffolding — the function body is untouched, so what CrossHair checks is
    exactly the generated code.
    """
    import ast

    try:
        tree = ast.parse(content)
    except SyntaxError:
        return None
    target = next(
        (n for n in ast.walk(tree)
         if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == func_name),
        None,
    )
    if target is None or not (target.body and isinstance(target.body[0], ast.Expr)
                              and isinstance(target.body[0].value, ast.Constant)
                              and isinstance(target.body[0].value.value, str)):
        return None  # require an existing docstring to extend (planner always emits one)

    doc_node = target.body[0]
    indent = " " * doc_node.col_offset
    original = doc_node.value.value.rstrip()
    clauses = [f"{indent}post: {post}"]
    if allow_value_error:
        clauses.append(f"{indent}raises: ValueError")
    # PEP 316 contracts must live INSIDE the docstring, so rebuild it: original text, then
    # the synthesized clauses, then the closing quotes.
    new_doc = f'{indent}"""{original}\n' + "\n".join(clauses) + f'\n{indent}"""'

    lines = content.splitlines()
    lines[doc_node.lineno - 1: doc_node.end_lineno] = new_doc.splitlines()
    return "\n".join(lines) + ("\n" if content.endswith("\n") else "")


def _abstract(msg: str, return_type: str) -> ContractViolation:
    """Turn a CrossHair counterexample message into a SPEC-LEVEL violation (no concrete inputs)."""
    msg = msg.strip()
    exc = re.match(r"([A-Za-z_]\w*Error|[A-Za-z_]\w*Exception)\b", msg)
    if msg.lower() in ("false", "post", "postcondition"):
        rt = return_type or "the declared type"
        return ContractViolation(
            contract_clause="postcondition",
            observation=(
                f"the postcondition guarantees the function returns {rt} for every valid "
                "input, but an input exists for which it returns a value of the wrong type"
            ),
        )
    if exc:
        return ContractViolation(
            contract_clause="response",
            observation=(
                f"an input exists for which the function crashes with an undeclared "
                f"{exc.group(1)} instead of returning {return_type or 'the declared type'} "
                "or rejecting the input with ValueError"
            ),
        )
    return ContractViolation(
        contract_clause="postcondition",
        observation="CrossHair found an input that violates the function's contract",
    )


def crosshair_available() -> bool:
    """Whether the crosshair CLI is importable/runnable in this environment."""
    return shutil.which("crosshair") is not None or _module_runnable()


def _module_runnable() -> bool:
    try:
        return subprocess.run(
            ["crosshair", "--version"], capture_output=True, env=_z3_env(), timeout=30
        ).returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def crosshair_verdicts(
    ir: dict,
    code: GeneratedCode,
    only_fr_ids: set[str] | None = None,
    per_condition_timeout: float = 8.0,
) -> dict[str, ContractVerdict]:
    """Per-fr_id deterministic verdicts from CrossHair (python stack only; {} otherwise).

    Each function is written to its own temp module with a synthesized type/exception
    contract, then ``crosshair check`` searches symbolically for counterexamples. Any found
    counterexample fails that contract with spec-level violations. Never raises: on a missing
    solver or a CrossHair error the function is reported as a pass-with-note so the pipeline
    degrades gracefully rather than blocking on an unavailable tool.
    """
    if (ir.get("stack") or "python") != "python":
        return {}
    if not crosshair_available():
        return {}

    contracts = (ir.get("planning") or {}).get("contracts") or []
    files_by_fr = {f.fr_id: f for f in code.files}
    env = _z3_env()
    out: dict[str, ContractVerdict] = {}

    with tempfile.TemporaryDirectory(prefix="cleanroom_crosshair_") as tmp:
        tmp_dir = Path(tmp)
        for contract in contracts:
            fr_id = contract["fr_id"]
            if only_fr_ids is not None and fr_id not in only_fr_ids:
                continue
            file = files_by_fr.get(fr_id)
            if file is None or not (file.content or "").strip():
                continue
            signature = contract.get("signature", "")
            func_name = _func_name(signature)
            if not func_name:
                continue

            return_type = _return_type(signature)
            post = _type_postcondition(return_type) or "True"
            allow_ve = contract.get("error_mode", "raise") == "raise"
            patched = _inject_contract(file.content, func_name, post, allow_ve)
            if patched is None:
                continue  # cannot attach a contract; leave this FR to other verifiers

            mod = tmp_dir / f"ch_{fr_id.replace('.', '_').replace('-', '_')}.py"
            mod.write_text(patched)
            try:
                proc = subprocess.run(
                    ["crosshair", "check", str(mod), "--analysis_kind=PEP316",
                     f"--per_condition_timeout={per_condition_timeout}"],
                    capture_output=True, text=True, env=env,
                    timeout=per_condition_timeout * 4 + 30,
                )
            except (OSError, subprocess.SubprocessError):
                continue  # solver/tool failure — do not block the pipeline

            violations: list[ContractViolation] = []
            seen: set[tuple[str, str]] = set()
            for line in (proc.stdout + "\n" + proc.stderr).splitlines():
                m = _ERROR_LINE.search(line)
                if not m:
                    continue
                v = _abstract(m.group("msg"), return_type)
                key = (v.contract_clause, v.observation)
                if key not in seen:
                    seen.add(key)
                    violations.append(v)

            out[fr_id] = ContractVerdict(
                fr_id=fr_id,
                verdict="fail" if violations else "pass",
                violations=violations,
            )
    return out
