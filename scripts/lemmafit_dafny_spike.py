"""Stage-3 feasibility spike: can an LLM author *verifying* Dafny for one DineOut feature?

Seeds the model with LemmaFit's own shipped skills + the abstract Domain interface, asks for a
state-machine module derived ONLY from the feature's spec contracts (cleanroom), then runs the
real Dafny verifier and feeds proof errors back for up to N rounds. Reports verified / rounds.

Usage:  uv run python scripts/lemmafit_dafny_spike.py [feature_id] [model] [max_rounds]
"""

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from langchain_core.messages import HumanMessage, SystemMessage

from src.cleanroom.llms.callbacks.metric import GLOBAL_METRICS
from src.cleanroom.utils.cost import estimate_cost
from src.cleanroom.utils.dafny_verify import verify_dafny
from src.cleanroom.utils.lemmafit_spec import build_spec_entries
from src.cleanroom.utils.llm_client import get_llm
from src.cleanroom.utils.usage_log import append_usage_log


def log_usage(feature_id: str, model: str, status: str) -> None:
    """Append this spike's token usage to API_USAGE.md, like the pipeline does for runs."""
    in_tot, out_tot, calls = GLOBAL_METRICS.snapshot()
    used_model = GLOBAL_METRICS.model or model
    metrics = {
        "srs": f"spike:{feature_id}", "model": used_model, "total_seconds": 0.0,
        "tokens": {"input": in_tot, "output": out_tot, "total": in_tot + out_tot, "calls": calls},
        "cost_usd": round(estimate_cost(used_model, in_tot, out_tot), 6),
    }
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    append_usage_log(metrics, status=status,
                     run_id=f"spike-{feature_id}-{model}-{stamp}")
    print(f"  token usage: {in_tot} in / {out_tot} out / {calls} calls · ${metrics['cost_usd']} → API_USAGE.md")

PROJ = Path("outputs/lemmafit_dineout")
SKILLS = PROJ / ".claude" / "skills"

feature_id = sys.argv[1] if len(sys.argv) > 1 else "4.1"
model = sys.argv[2] if len(sys.argv) > 2 else "gpt-4o-mini"
max_rounds = int(sys.argv[3]) if len(sys.argv) > 3 else 5
mod = "F" + feature_id.replace(".", "_")          # e.g. F4_1


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


def strip_fences(text: str) -> str:
    m = re.search(r"```(?:dafny)?\s*(.*?)```", text, re.DOTALL)
    return (m.group(1) if m else text).strip()


ir = json.load(open("outputs/dineout_srs_full_ir.json"))
feat = next(f for f in ir["features"] if f["id"] == feature_id)
contracts = [c for c in ir["planning"]["contracts"] if c["feature_id"] == feature_id]
fr_ids = {c["fr_id"] for c in contracts}
spec_entries = [e for e in build_spec_entries(ir) if e["req_id"] in fr_ids]

domain_iface = (PROJ / "lemmafit" / "dafny" / "Replay.dfy").read_text().split(
    "abstract module {:compile false} Kernel")[0]
dafny_skill = (SKILLS / "lemmafit-dafny" / "SKILL.md").read_text()
proofs_skill = (SKILLS / "lemmafit-proofs" / "SKILL.md").read_text()

system = f"""You are a Dafny author for LemmaFit. Produce ONE Dafny module that refines the
abstract `Domain` below into a verified state machine. Output ONLY Dafny source — no markdown,
no prose, no code fences.

CRITICAL GOTCHA: a refining `Apply` function and the refining `StepPreservesInv` lemma must NOT
repeat `requires Inv(m)` — it is inherited from the abstract Domain and repeating it is an error.

{DAFNY_REF}

=== ABSTRACT DOMAIN INTERFACE (you must refine this; do not redefine it) ===
{domain_iface}

=== SKILL: lemmafit-dafny ===
{dafny_skill}

=== SKILL: lemmafit-proofs ===
{proofs_skill}
"""

contract_lines = []
for c in contracts:
    bc = c.get("contract") or {}
    contract_lines.append(
        f"- FR {c['fr_id']}: stimulus={bc.get('stimulus','')!r}; precondition={bc.get('precondition','')!r}; "
        f"response={bc.get('response','')!r}; postcondition={bc.get('postcondition','')!r}")
spec_lines = [f"- [{e['type']}] {e['property']}" for e in spec_entries]

user = f"""Feature {feature_id}: {feat.get('name','')}

Functional requirements (each becomes an Action variant):
{chr(10).join(contract_lines)}

SPEC.yaml properties to back with lemmas (postconditions need a matching `ensures` lemma):
{chr(10).join(spec_lines)}

Write a file that:
- starts with: include "Replay.dfy"
- defines `module {mod}Domain refines Domain {{ ... }}` with: a concrete `type Model`; a
  `datatype Action` with ONE variant per FR; `ghost predicate Inv`; `function Init`;
  `function Apply` (one match case per Action — NO `requires`); `function Normalize` (repair to
  satisfy Inv); the lemmas `InitSatisfiesInv` and `StepPreservesInv` (NO `requires`); and at
  least one domain-specific postcondition lemma with an `ensures` matching a SPEC property above.
- defines `module {mod}Kernel refines Kernel {{ import D = {mod}Domain }}`
Derive everything ONLY from the spec above. Output ONLY the Dafny source.
"""

llm = get_llm(model=model, temperature=0.0)
messages = [SystemMessage(system), HumanMessage(user)]
target = PROJ / "lemmafit" / "dafny" / f"{mod}Gen.dfy"

print(f"=== Stage-3 spike: feature {feature_id} ({feat.get('name','')}) · model={model} · ≤{max_rounds} rounds ===")
for rnd in range(1, max_rounds + 1):
    resp = llm.invoke(messages)
    code = strip_fences(resp.content if isinstance(resp.content, str) else str(resp.content))
    target.write_text(code)
    res = verify_dafny(target)
    print(f"  round {rnd}: ok={res.ok}  verified={res.verified}  errors={res.errors}")
    if res.ok:
        print(f"\nVERIFIED in {rnd} round(s) → {target}")
        log_usage(feature_id, model, status=f"spike-verified ({rnd}r)")
        sys.exit(0)
    errs = "\n".join(f"  line {m['line']}: {m['message']}" for m in res.messages[:12])
    print(errs)
    messages.append(resp)
    messages.append(HumanMessage(
        f"`dafny verify` failed with these errors:\n{errs}\n\nOutput the FULL corrected Dafny "
        "module (only Dafny source). Remember: do not repeat `requires Inv(m)` on refining "
        "Apply/StepPreservesInv."))

print(f"\nNOT verified after {max_rounds} rounds. Last errors above. File: {target}")
log_usage(feature_id, model, status=f"spike-unverified ({max_rounds}r)")
sys.exit(1)
