"""Spec reader for the Test Agent.

Deterministic, no LLM. This is the ONLY place the Test Agent touches the IR, and
it reads strictly from the SPECIFICATION: ir['features'] and the requirements
within. It never looks at 'generated_code', 'dependency_graph', or
'increment_plan' — the Test Agent must derive tests from what the software should
do, not from anything the Code Agent produced.
"""


def feature_of(req_id: str) -> str:
    """Feature id is the first two dot-segments of a requirement id: '2.2.6.6' -> '2.2'."""
    return ".".join(req_id.split(".")[:2])


def feature_units(ir: dict) -> list[dict]:
    """Slice the specification into one scoped unit per feature.

    Each unit carries only that feature's own spec content (id, name, description,
    and its requirements). Features with no requirements yield nothing to test and
    are skipped. Reads ONLY ir['features'].
    """
    units: list[dict] = []
    for feature in ir.get("features", []):
        requirements = feature.get("functional_requirements", [])
        if not requirements:
            continue
        units.append(
            {
                "feature_id": feature_of(requirements[0]["id"]),
                "name": feature.get("name", ""),
                "description": feature.get("description", ""),
                "requirements": [
                    {"id": r["id"], "description": r.get("description", "")} for r in requirements
                ],
            }
        )
    return units
