from typing import ClassVar, Literal

from pydantic import BaseModel, Field


class TestVerdict(BaseModel):
    # Keep pytest from collecting this model as a test (its name starts with "Test").
    __test__: ClassVar[bool] = False

    requirement_id: str = Field(description="The requirement/test case this verdict is for, e.g. '2.2.1'")
    verdict: Literal["pass", "fail"] = Field(description="Whether the code satisfies this test case")
    reason: str = Field(default="", description="Brief justification for the verdict")


class FeatureJudgement(BaseModel):
    """The LLM judge's output for one (code sample, feature): one verdict per test case."""

    verdicts: list[TestVerdict] = Field(default_factory=list)


class FeatureCertification(BaseModel):
    """pass@k results for a single feature."""

    feature_id: str
    name: str = ""
    n_samples: int = Field(description="n: code samples generated for this feature")
    n_test_cases: int = Field(description="number of spec-derived test cases used as the oracle")
    passing_samples: int = Field(description="c: samples that passed ALL of the feature's test cases")
    pass_at: dict[str, float] = Field(default_factory=dict, description="e.g. {'pass@1': 0.4, 'pass@5': 1.0}")


class CertificationResult(BaseModel):
    model: str = ""
    n: int = Field(description="samples generated per feature")
    k_values: list[int] = Field(default_factory=list)
    features: list[FeatureCertification] = Field(default_factory=list)
    aggregate_pass_at: dict[str, float] = Field(
        default_factory=dict, description="mean pass@k across features"
    )
    notes: list[str] = Field(default_factory=list)
