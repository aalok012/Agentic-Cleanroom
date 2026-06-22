"""The Dafny proof track: generate VERIFIED Dafny per feature (no LemmaFit dependency).

For each feature it casts the FRs into a Dafny ``Domain`` state machine (one ``Action`` per FR;
BehavioralContract -> Inv / precondition guards / postcondition lemmas) that refines our vendored
``Replay.dfy`` kernel, then runs the real Dafny verifier and feeds proof errors back for up to
``max_rounds`` rounds — the generate->verify->revise loop validated by the feasibility spikes
(needs a gpt-4.1-class model; gpt-4o-mini/gpt-4o cannot discharge map-comprehension proofs).

Prompt knowledge is OWNED here (DAFNY_REF syntax + PROOF_REF tactics), folded in from the former
LemmaFit skills — no ``.claude/skills`` files are read.

Isolation: the agent derives everything ONLY from the spec (FR text + behavioral contracts +
SPEC.yaml entries) and never reads tests or any generated test artifact — the same clean-room
guarantee as the Python Code Agent, just targeting Dafny.
"""

from __future__ import annotations

import re
from pathlib import Path

from langchain_core.messages import HumanMessage, SystemMessage

from src.cleanroom.agents.dafny.schema.dafny import FeatureDafny, GeneratedDafny
from src.cleanroom.utils.dafny_verify import verify_dafny
from src.cleanroom.utils.dafny_spec import build_spec_entries, build_spec_yaml
from src.cleanroom.utils.llm_client import get_llm

# Dafny constructs models routinely get wrong; priming these turned an infinite syntax loop
# into actual progress in the feasibility spikes.
DAFNY_REF = """=== DAFNY SYNTAX REFERENCE (use these EXACT forms; wrong forms cause "gets expected"/"closeparen expected") ===
- Record type: use a datatype, NOT a named tuple:  datatype Item = Item(name: string, price: int)
- Map type:        map<string, int>
- Map update:      m[k := v]                  // add or overwrite one entry
- Map removal:     m - {k}                    // remove a key (the RHS is a SET literal)
- Map membership:  k in m   /   k !in m
- Map lookup:      m[k]      (only valid when k in m)
- Map comprehension (filter/transform): map k | k in m && <predicate> :: m[k]
  e.g. keep non-empty entries:  map k | k in m && k != "" && m[k] != "" :: m[k]
- Sequence: s + [x] (append), s[1..] (tail), |s| (length), s[i] (index)
- match: each case on its own line; NO `requires` inside Apply.
- Quantifiers & comprehensions use `|` for the RANGE and `::` for the BODY/term — NEVER `::` twice:
    forall x | P(x) :: Q(x)        (WRONG: `forall x :: P :: Q`)
    exists x | P(x) :: Q(x)
    set x | x in S :: f(x)         (every bound var MUST appear in the range; MUST end with a term)
    map k | k in m :: f(k)
  Flatten nested sets with MULTIPLE bound vars: set o, d | o in orders && d in orders[o] :: d
- Functions are PURE: NO reassignment. `var x := e; <expr>` is a one-shot let-binding — you may
  NOT then write `x := e2;`. Use fresh names / nested `var` lets instead.
- Every `if ... then ...` in a function MUST have an `else` (functions are total).
- Empty literals: empty map is `map[]`, empty set is `{}`, empty seq is `[]` — NEVER `set {}` or `map []`."""

# Proof tactics, folded in from the former LemmaFit `lemmafit-proofs` skill (now owned in-repo).
PROOF_REF = """=== DAFNY PROOF TACTICS ===
- Postconditions first: write the `ensures` (the guarantee) before the body.
- For a map lookup `m[k]`, you MUST first establish `k in m` (assert it, or add it as a
  precondition / guard) — otherwise Dafny reports "function precondition could not be proved".
- For "if X then Y", also reason about "if not X" — one-directional claims leave gaps.
- Tighten `Inv`: every clamp/guard in code (e.g. `if x > MAX then MAX else x`) should have a
  matching bound in `Inv` (e.g. `0 <= x <= MAX`).
- Prove a domain-specific postcondition lemma per Action (something stronger than the generic
  StepPreservesInv), with an `ensures` matching a SPEC property.
- LAST RESORT only: if an obligation is genuinely infeasible to prove, you may write
  `assume {:axiom} <expr>;` with a one-line comment justifying why — this passes the proof as an
  explicit, auditable ASSUMPTION rather than a discharged lemma. Prefer a real proof."""

_SYSTEM = """You are a Dafny author. Produce ONE Dafny file that refines the abstract `Domain`
below into a verified state machine for a single feature. Output ONLY Dafny source — no markdown,
no prose, no code fences.

CRITICAL GOTCHA: a refining `Apply` function and the refining `StepPreservesInv` lemma must NOT
repeat `requires Inv(m)` — it is inherited from the abstract Domain and repeating it is an error.

{ref}

{proofs}

=== ABSTRACT DOMAIN INTERFACE (refine this; do not redefine it) ===
{domain}
"""


def _strip_fences(text: str) -> str:
    m = re.search(r"```(?:dafny)?\s*(.*?)```", text, re.DOTALL)
    return (m.group(1) if m else text).strip()


class DafnyAgent:
    """Generate verified Dafny modules from spec contracts, one per feature."""

    def __init__(self, project_dir: Path | str, llm=None, model: str = "gpt-4.1",
                 max_rounds: int = 6) -> None:
        self.project_dir = Path(project_dir)
        self.dafny_dir = self.project_dir / "dafny"
        self.model = model
        self.max_rounds = max_rounds
        self.llm = llm or get_llm(model=model, temperature=0.0)
        self._system = self._build_system()

    def _build_system(self) -> str:
        domain = (self.dafny_dir / "Replay.dfy").read_text().split(
            "abstract module {:compile false} Kernel")[0]
        return _SYSTEM.format(ref=DAFNY_REF, proofs=PROOF_REF, domain=domain)

    def _feature_prompt(self, ir: dict, feature_id: str, mod: str) -> str:
        feat = next((f for f in ir.get("features", []) if f.get("id") == feature_id), {})
        contracts = [c for c in (ir.get("planning") or {}).get("contracts", [])
                     if c.get("feature_id") == feature_id]
        fr_ids = {c["fr_id"] for c in contracts}
        spec = [e for e in build_spec_entries(ir) if e["req_id"] in fr_ids]

        clines = []
        for c in contracts:
            bc = c.get("contract") or {}
            clines.append(
                f"- FR {c['fr_id']}: stimulus={bc.get('stimulus','')!r}; "
                f"precondition={bc.get('precondition','')!r}; response={bc.get('response','')!r}; "
                f"postcondition={bc.get('postcondition','')!r}")
        slines = [f"- [{e['type']}] {e['property']}" for e in spec]

        return (
            f"Feature {feature_id}: {feat.get('name','')}\n\n"
            f"Functional requirements (each becomes an Action variant):\n" + "\n".join(clines) +
            "\n\nSPEC.yaml properties to back with lemmas (postconditions need a matching `ensures`):\n"
            + "\n".join(slines) + "\n\n"
            'Write a file that: starts with `include "Replay.dfy"`; defines '
            f"`module {mod}Domain refines Domain {{ ... }}` with a concrete `type Model`, a "
            "`datatype Action` (ONE variant per FR), `ghost predicate Inv`, `function Init`, "
            "`function Apply` (one match case per Action — NO `requires`), `function Normalize` "
            "(repair to satisfy Inv), lemmas `InitSatisfiesInv` and `StepPreservesInv` (NO "
            "`requires`), and at least one domain-specific postcondition lemma with an `ensures` "
            f"matching a SPEC property above; and defines `module {mod}Kernel refines Kernel "
            f"{{ import D = {mod}Domain }}`. Derive everything ONLY from the spec above. "
            "Output ONLY the Dafny source.")

    def generate_feature(self, ir: dict, feature_id: str) -> FeatureDafny:
        mod = "F" + feature_id.replace(".", "_")
        target = self.dafny_dir / f"{mod}.dfy"
        messages = [SystemMessage(self._system), HumanMessage(self._feature_prompt(ir, feature_id, mod))]

        last = FeatureDafny(feature_id=feature_id, module=mod, dafny_source="", verified=False)
        for rnd in range(1, self.max_rounds + 1):
            resp = self.llm.invoke(messages)
            code = _strip_fences(resp.content if isinstance(resp.content, str) else str(resp.content))
            target.write_text(code)
            res = verify_dafny(target)
            last = FeatureDafny(feature_id=feature_id, module=mod, dafny_source=code,
                                verified=res.ok, rounds=rnd, residual_errors=res.messages,
                                axioms=res.axioms)
            if res.ok:
                return last
            errs = "\n".join(f"  line {m['line']}: {m['message']}" for m in res.messages[:12])
            messages.append(resp)
            messages.append(HumanMessage(
                f"`dafny verify` failed with these errors:\n{errs}\n\nOutput the FULL corrected "
                "Dafny module (only Dafny source). Do not repeat `requires Inv(m)` on refining "
                "Apply/StepPreservesInv."))
        return last

    def generate(self, ir: dict) -> GeneratedDafny:
        feature_ids = sorted({c["feature_id"] for c in (ir.get("planning") or {}).get("contracts", [])})
        features = [self.generate_feature(ir, fid) for fid in feature_ids]
        return GeneratedDafny(features=features, spec_yaml=build_spec_yaml(ir))
