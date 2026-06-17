from typing import ClassVar

from pydantic import BaseModel, Field


class TestCase(BaseModel):
    # __test__ = False keeps pytest from trying to collect this model as a test
    # class when it is imported into a test module (its name starts with "Test").
    __test__: ClassVar[bool] = False

    requirement_id: str = Field(description="The requirement this case verifies, e.g. '2.2.1'")
    description: str = Field(description="What behavior is being checked")
    inputs: str = Field(description="Concrete example inputs, specific enough to execute later")
    expected: str = Field(description="Expected output/result per the requirement (the pass condition)")


class FeatureTests(BaseModel):
    feature_id: str = Field(description="Feature these cases belong to, e.g. '2.2'")
    cases: list[TestCase] = Field(default_factory=list)


class GeneratedTests(BaseModel):
    features: list[FeatureTests] = Field(default_factory=list)
