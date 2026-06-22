"""Map the cleanroom IR's behavioral contracts onto a LemmaFit ``SPEC.yaml``.

LemmaFit's workflow is "SPEC.yaml first": every verifiable behavior is a structured entry
(precondition / postcondition / invariant) that a Dafny module must then formalize and prove.
Our spec stage already extracts exactly that information per FR — stimulus, precondition,
response, postcondition — so this converts it deterministically into SPEC.yaml entries, one
``precondition`` and one ``postcondition`` entry per FR that declares them.

The formal ``property`` expression is left as the contract's prose with ``state: DRAFT`` — the
Dafny stage (LLM) formalizes it into a Dafny predicate/ensures clause and flips it to
``ADDRESSED`` once it verifies. This step is mechanical and spec-derived (never reads tests or
generated code), so the cleanroom isolation holds. See the LemmaFit ``lemmafit-spec`` skill for
the schema this targets.
"""

from __future__ import annotations

import yaml

# Values that mean "no real precondition/postcondition" and should not produce an entry.
_EMPTY = {"", "none", "n/a", "na", "null", "-"}


def _meaningful(text: str | None) -> bool:
    return bool(text) and text.strip().lower() not in _EMPTY


def _module_for(feature_id: str) -> str:
    """A valid Dafny module name for a feature's state machine, e.g. '4.1' -> 'Core_4_1'."""
    return "Core_" + "".join(c if c.isalnum() else "_" for c in feature_id)


def build_spec_entries(ir: dict) -> list[dict]:
    """SPEC.yaml ``entries`` list derived from the planning contracts' behavioral contracts."""
    contracts = (ir.get("planning") or {}).get("contracts") or []
    feature_names = {f.get("id"): f.get("name", "") for f in ir.get("features", [])}

    entries: list[dict] = []
    post_id_by_fr: dict[str, str] = {}      # fr_id -> its postcondition spec id (for depends_on)
    n = 0

    def _new_id() -> str:
        nonlocal n
        n += 1
        return f"spec-{n:03d}"

    # First pass: precondition + postcondition entries, recording each FR's postcondition id.
    for c in contracts:
        fr_id = c.get("fr_id", "")
        feat = c.get("feature_id", "")
        bc = c.get("contract") or {}
        module = _module_for(feat)
        group = feature_names.get(feat) or "Business Logic"

        if _meaningful(bc.get("precondition")):
            entries.append({
                "id": _new_id(), "req_id": fr_id,
                "title": f"Precondition of {fr_id}: {bc['precondition'].strip()}",
                "group": group, "layer": "logic", "type": "precondition",
                "property": bc["precondition"].strip(),
                "module": module, "depends_on": [],
                "verifiable": True, "guarantee_type": "verified", "state": "DRAFT",
            })

        response = (bc.get("response") or "").strip()
        postcondition = (bc.get("postcondition") or "").strip()
        guarantee = postcondition if _meaningful(postcondition) else response
        if _meaningful(guarantee):
            sid = _new_id()
            post_id_by_fr[fr_id] = sid
            entries.append({
                "id": sid, "req_id": fr_id,
                "title": f"Postcondition of {fr_id}: {guarantee}",
                "group": group, "layer": "logic", "type": "postcondition",
                "property": guarantee,
                "module": module, "depends_on": [],
                "verifiable": True, "guarantee_type": "verified", "state": "DRAFT",
            })

    # Second pass: link each postcondition's depends_on to its prerequisites' postconditions.
    by_fr = {c.get("fr_id"): c for c in contracts}
    for c in contracts:
        sid = post_id_by_fr.get(c.get("fr_id"))
        if not sid:
            continue
        deps = [post_id_by_fr[p] for p in c.get("prerequisite_fr_ids", []) if p in post_id_by_fr]
        if deps:
            for e in entries:
                if e["id"] == sid:
                    e["depends_on"] = deps
                    break

    return entries


def build_spec_yaml(ir: dict) -> str:
    """The full ``SPEC.yaml`` document text for an IR."""
    return yaml.safe_dump({"entries": build_spec_entries(ir)}, sort_keys=False, width=100)
