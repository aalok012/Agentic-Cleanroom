"""Drive the Dafny verifier synchronously for the LemmaFit/TypeScript stack.

LemmaFit ships a Dafny toolchain (downloaded by ``npm install`` into ``~/.lemmafit/.dafny``).
Its daemon watches files and verifies on change, which suits interactive Claude Code but not a
batch pipeline; for the generate->verify->revise loop we instead invoke ``dafny verify``
directly and parse its result. This module is the Stage-4 core: locate the binary, run it on a
``.dfy`` file, and return a structured pass/fail + the proof errors to feed back to the agent.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

# "Dafny program verifier finished with 10 verified, 0 errors"
_SUMMARY = re.compile(r"finished with (\d+) verified, (\d+) error", re.IGNORECASE)
# "path.dfy(30,16): Error: a refining function is not allowed to add preconditions"
_ERROR_LINE = re.compile(r"\((\d+),(\d+)\):\s*(?:Error|.*?error)\b[:]?\s*(.*)", re.IGNORECASE)

# Where LemmaFit's npm postinstall puts the Dafny launcher, plus the usual fallbacks.
_DAFNY_PROBES = (
    Path.home() / ".lemmafit" / ".dafny" / "dafny" / "dafny",
)


@dataclass
class DafnyResult:
    ok: bool
    verified: int = 0
    errors: int = 0
    messages: list[dict] = field(default_factory=list)   # [{line, col, message}]
    raw: str = ""


def dafny_binary() -> str | None:
    """Path to a runnable ``dafny`` launcher: $DAFNY, the LemmaFit download, or PATH."""
    env = os.environ.get("DAFNY")
    if env and Path(env).exists():
        return env
    for p in _DAFNY_PROBES:
        if p.exists():
            return str(p)
    return shutil.which("dafny")


def dafny_available() -> bool:
    return dafny_binary() is not None


def verify_dafny(dfy_path: Path | str, timeout: float = 180.0) -> DafnyResult:
    """Run ``dafny verify`` on a file and parse the verdict + proof errors.

    Never raises on a verification failure — a failed proof is data, returned in the result.
    Raises only if the Dafny binary cannot be found (a setup error, not a proof outcome).
    """
    binary = dafny_binary()
    if binary is None:
        raise RuntimeError("dafny binary not found (run `npm install` in a `lemmafit init` project)")

    try:
        proc = subprocess.run(
            # --allow-warnings: Dafny exits non-zero on STYLE warnings (e.g. ==> indentation)
            # even when verification fully succeeds; we judge by the verification summary, not
            # warnings, so they must not be treated as a failure.
            [binary, "verify", "--allow-warnings", str(dfy_path)],
            capture_output=True, text=True, timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return DafnyResult(ok=False, errors=1,
                           messages=[{"line": 0, "col": 0, "message": "dafny verify timed out"}],
                           raw="timeout")

    out = (proc.stdout or "") + "\n" + (proc.stderr or "")
    summary = _SUMMARY.search(out)
    verified = int(summary.group(1)) if summary else 0
    errors = int(summary.group(2)) if summary else 0

    messages: list[dict] = []
    for line in out.splitlines():
        m = _ERROR_LINE.search(line)
        if m:
            messages.append({"line": int(m.group(1)), "col": int(m.group(2)),
                             "message": m.group(3).strip()})

    # Judge by the verification summary, NOT the exit code: Dafny exits non-zero on mere style
    # warnings even when every proof obligation is discharged. Pass iff a clean summary with zero
    # verification errors and no error-location lines.
    ok = summary is not None and errors == 0 and not messages
    # No summary at all => a resolution/parse error (nothing was verified); capture it as a failure.
    if summary is None and not messages:
        messages.append({"line": 0, "col": 0, "message": out.strip()[:300] or "dafny produced no output"})
        ok = False
    return DafnyResult(ok=ok, verified=verified, errors=max(errors, len(messages)),
                       messages=messages, raw=out)
