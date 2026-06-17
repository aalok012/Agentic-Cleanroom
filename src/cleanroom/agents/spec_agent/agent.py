"""Specification Generator Agent.

Stage 1 of the pipeline, with two cleanly separated responsibilities:

  1. STRUCTURE (deterministic, via SRSReader): parse the SRS, assign stable IDs, group
     requirements into features. The LLM is intentionally kept OUT of this so IDs, text,
     and grouping can never drift, be dropped, or be hallucinated. `run()` owns this and
     emits every parsed requirement under `functional_requirements` as a starting point.

  2. CLASSIFICATION (LLM, via enrich): per feature, label each already-extracted
     requirement as FR (functional) or NFR (non-functional quality/constraint), and attach
     a category + rationale to every NFR. One structured LLM call PER FEATURE, sending only
     that feature's requirements — never the whole IR.

The LLM only ever returns labels keyed by id; the requirement id and text always come from
the parser, and any id the parser did not produce is ignored. NFRs stay attached to their
feature (each feature carries both `functional_requirements` and `non_functional_requirements`).
"""

import json
from pathlib import Path

from src.cleanroom.agents.spec_agent.schema.ir import (
    NFR_CATEGORIES,
    Feature,
    FeatureClassification,
    FunctionalRequirement,
    IntermediateRepresentation,
    NonFunctionalRequirement,
)
from src.cleanroom.agents.spec_agent.tools.srs_reader import SRSReader
from src.cleanroom.utils.llm_client import get_llm
from src.cleanroom.utils.prompt_renderer import PromptRenderer

_VALID_CATEGORIES = set(NFR_CATEGORIES)


class SpecAgent:
    def __init__(self) -> None:
        self.llm = get_llm()
        self.renderer = PromptRenderer()
        self.reader = SRSReader()

    # ------------------------------------------------------------------
    # 1. deterministic structure
    # ------------------------------------------------------------------
    def run(self, srs_path: Path, output_dir: Path = Path("outputs")) -> IntermediateRepresentation:
        """Parse the SRS deterministically. Every parsed requirement starts life as an
        FR; enrich() reclassifies them. No LLM here."""
        feature_dicts = self.reader.read_features(srs_path)

        features = []
        for f in feature_dicts:
            reqs = f.get("functional_requirements", [])
            description = f.get("description", "")
            # Leaf sections (e.g. Security, Privacy, Vocabulary) carry their requirement
            # text in the section body, not as child requirements. Surface that body as a
            # single requirement (id = section id) so it is visible to FR/NFR classification
            # — otherwise these whole-section quality requirements would be invisible.
            if not reqs and description.strip():
                reqs = [{"id": f["feature_id"], "description": description}]
            features.append(
                Feature(
                    id=f["feature_id"],
                    name=f["name"],
                    description=description,
                    functional_requirements=[
                        FunctionalRequirement(id=req["id"], text=req["description"]) for req in reqs
                    ],
                )
            )

        ir = IntermediateRepresentation(
            project_name=srs_path.stem,
            source_file=srs_path.name,
            features=features,
            specifications=[],
            extraction_notes=[],
        )

        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / f"{srs_path.stem}_ir.json").write_text(ir.model_dump_json(indent=2))
        return ir

    # ------------------------------------------------------------------
    # 2. LLM classification (per feature)
    # ------------------------------------------------------------------
    def enrich(self, ir: dict, output_dir: Path = Path("outputs")) -> dict:
        """Classify each feature's requirements into FR/NFR (one LLM call per feature).

        Returns a NEW IR dict (the input is not mutated) where every feature carries both
        `functional_requirements` and `non_functional_requirements`. Also writes the
        FR/NFR breakdown to outputs/<project>_fr_nfr.json.
        """
        new_features: list[dict] = []
        breakdown: list[dict] = []

        for feature in ir.get("features", []):
            # In the base IR every requirement sits under functional_requirements.
            candidates = feature.get("functional_requirements", [])
            frs, nfrs = self._classify_feature(feature.get("name", ""), candidates)

            new_features.append(
                {
                    **feature,
                    "functional_requirements": [fr.model_dump() for fr in frs],
                    "non_functional_requirements": [nfr.model_dump() for nfr in nfrs],
                }
            )
            breakdown.append(
                {
                    "feature_id": feature.get("id", ""),
                    "name": feature.get("name", ""),
                    "functional_requirements": [fr.model_dump() for fr in frs],
                    "non_functional_requirements": [nfr.model_dump() for nfr in nfrs],
                }
            )

        enriched = {**ir, "features": new_features}

        output_dir.mkdir(parents=True, exist_ok=True)
        dest = output_dir / f"{ir.get('project_name', 'project')}_fr_nfr.json"
        dest.write_text(json.dumps({"features": breakdown}, indent=2))
        return enriched

    def _classify_feature(
        self, feature_name: str, requirements: list[dict]
    ) -> tuple[list[FunctionalRequirement], list[NonFunctionalRequirement]]:
        """One structured LLM call for a single feature's requirements."""
        if not requirements:
            return [], []

        prompt = self.renderer.render(
            "classify_requirements.j2",
            {"feature_name": feature_name, "requirements": requirements},
        )
        result: FeatureClassification = self.llm.with_structured_output(FeatureClassification).invoke(prompt)
        # The model often echoes the id in the prompt's "[id]" form; normalize so it
        # matches the parser's bare id (otherwise a miss would silently default to FR).
        labels = {_norm_id(c.id): c for c in result.classifications}

        frs: list[FunctionalRequirement] = []
        nfrs: list[NonFunctionalRequirement] = []
        for req in requirements:
            rid, text = req["id"], req.get("text", req.get("description", ""))
            label = labels.get(rid)
            if label is not None and label.kind == "NFR":
                category = label.category if label.category in _VALID_CATEGORIES else "other"
                rationale = (label.rationale or "").strip() or (
                    f"{category.capitalize()} constraint the implementation must satisfy (requirement {rid})."
                )
                nfrs.append(
                    NonFunctionalRequirement(id=rid, text=text, category=category, rationale=rationale)
                )
            else:
                # Default to FR when unlabeled or labeled FR — safe, never drops a requirement.
                frs.append(FunctionalRequirement(id=rid, text=text))
        return frs, nfrs


def _norm_id(raw: str) -> str:
    """Normalize an id the LLM echoed back (e.g. '[2.7.2]' or ' 2.7.2 ') to bare '2.7.2'."""
    return (raw or "").strip().strip("[]").strip()
