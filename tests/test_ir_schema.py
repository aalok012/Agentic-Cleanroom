"""Schema alignment tests — canonical IR fields and model round-trips."""

import json

import pytest
from pydantic import ValidationError

from src.cleanroom.agents.evaluation.agent import CertificationAgent
from src.cleanroom.agents.evaluation.schema.certification import (
    CertificationResult,
    FRCertification,
    FeatureCertification,
)
from src.cleanroom.agents.spec_agent.schema.ir import EnrichedIR, IntermediateRepresentation
from src.cleanroom.agents.test.schema.tests import GeneratedTests, TestCase
from src.cleanroom.utils.ir import (
    feature_id_of,
    normalize_feature,
    normalize_fr,
    normalize_generated_tests,
    normalize_ir,
    normalize_ir_features,
    normalize_test_case,
    requirement_text,
)


def test_legacy_feature_id_normalized_to_id():
    legacy = {
        "feature_id": "3.1",
        "name": "Torrent Search",
        "functional_requirements": [{"id": "3.1.REQ-1", "description": "Search."}],
    }
    out = normalize_feature(legacy)
    assert out["id"] == "3.1"
    assert "feature_id" not in out
    assert out["functional_requirements"][0]["text"] == "Search."


def test_requirement_text_prefers_text_over_description():
    assert requirement_text({"text": "canonical", "description": "legacy"}) == "canonical"
    assert requirement_text({"description": "legacy only"}) == "legacy only"


def test_normalize_test_case_defaults_oracle_fields():
    case = normalize_test_case({"requirement_id": "3.1.REQ-1"})
    assert case["inputs_json"] == "{}"
    assert case["expected_json"] == "null"
    assert case["oracle"] == "eq"


def test_normalize_generated_tests_in_place():
    tests = {
        "features": [{
            "feature_id": "3.1",
            "cases": [{"requirement_id": "3.1.REQ-1"}],
        }]
    }
    normalize_generated_tests(tests)
    assert tests["features"][0]["cases"][0]["inputs_json"] == "{}"


def test_certification_result_preserves_aggregate_case_pass_rate():
    result = CertificationResult(
        model="gpt-4o-mini",
        n=1,
        k_values=[1],
        frs=[
            FRCertification(
                fr_id="3.1.REQ-1",
                feature_id="3.1",
                n_samples=1,
                n_test_cases=2,
                passing_samples=1,
                pass_at={"pass@1": 1.0},
                cases_passed=2,
                cases_total=2,
                case_pass_rate=1.0,
            )
        ],
        features=[
            FeatureCertification(
                feature_id="3.1",
                name="Torrent Search",
                n_samples=1,
                n_test_cases=2,
                passing_samples=1,
                pass_at={"pass@1": 1.0},
                cases_passed=2,
                cases_total=2,
                case_pass_rate=1.0,
            )
        ],
        aggregate_pass_at={"pass@1": 1.0},
        aggregate_case_pass_rate=1.0,
    )
    dumped = result.model_dump()
    assert dumped["aggregate_case_pass_rate"] == 1.0
    restored = CertificationResult(**dumped)
    assert restored.aggregate_case_pass_rate == 1.0


def test_enriched_ir_accepts_pipeline_keys():
    ir = normalize_ir({
        "project_name": "demo",
        "source_file": "demo.xml",
        "features": [{
            "id": "3.1",
            "name": "Feature",
            "functional_requirements": [{"id": "3.1.REQ-1", "text": "Do thing."}],
        }],
        "contracts": [],
        "planning": {"contracts": []},
        "generated_code": {"files": []},
        "generated_tests": {"features": []},
        "certification": {"n": 1, "k_values": [1], "aggregate_case_pass_rate": 0.0},
    })
    model = EnrichedIR.model_validate(ir)
    assert feature_id_of(model.features[0].model_dump()) == "3.1"


def test_intermediate_representation_rejects_legacy_feature_id():
    with pytest.raises(ValidationError):
        IntermediateRepresentation(
            project_name="demo",
            source_file="demo.xml",
            features=[{
                "feature_id": "3.1",
                "name": "Feature",
                "functional_requirements": [{"id": "3.1.REQ-1", "description": "x"}],
            }],
        )


def test_cases_by_fr_normalizes_legacy_cases():
    tests = {
        "features": [{
            "feature_id": "3.1",
            "cases": [{"requirement_id": "3.1.REQ-1", "description": "happy path"}],
        }]
    }
    by_fr = CertificationAgent._cases_by_fr(tests)
    case = by_fr["3.1.REQ-1"][0]
    assert case["inputs_json"] == "{}"
    assert case["expected_json"] == "null"


def test_generated_tests_schema_round_trip():
    tests = GeneratedTests(features=[
        {
            "feature_id": "3.1",
            "cases": [
                TestCase(
                    requirement_id="3.1.REQ-1",
                    description="Search works",
                    inputs="query=x",
                    expected="results",
                    inputs_json='{"query":"x"}',
                    expected_json="[]",
                )
            ],
        }
    ])
    restored = GeneratedTests(**json.loads(tests.model_dump_json()))
    assert restored.features[0].cases[0].inputs_json == '{"query":"x"}'


def test_normalize_ir_features_idempotent():
    ir = {
        "features": [{
            "id": "3.1",
            "name": "F",
            "functional_requirements": [{"id": "3.1.REQ-1", "text": "t"}],
        }]
    }
    normalize_ir_features(ir)
    once = json.dumps(ir)
    normalize_ir_features(ir)
    assert json.dumps(ir) == once
