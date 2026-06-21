from typing import ClassVar, Literal

from pydantic import BaseModel, Field


class TestCase(BaseModel):
    __test__: ClassVar[bool] = False

    requirement_id: str = Field(description="The requirement this case verifies, e.g. '2.2.1'")
    description: str = Field(description="What behavior is being checked")
    inputs: str = Field(description="Human-readable summary of inputs")
    expected: str = Field(description="Human-readable summary of expected result")
    inputs_json: str = Field(
        description='JSON object of keyword arguments, e.g. {"query": "pizza"}'
    )
    expected_json: str = Field(
        description='JSON expected return, or {"raises": "ValueError"} for failure cases'
    )
    oracle: Literal["eq", "raises"] = Field(
        default="eq", description="eq = assert return equals expected_json; raises = expect exception"
    )
    setup_json: str = Field(
        default="",
        description=(
            "FastAPI stack only: a JSON array of Arrange calls that establish this case's "
            'precondition state before the main call, e.g. for "edit an existing staff member" '
            '[{"inputs": {"action": "add", "staff_member": {"id": 1, "name": "Ann"}}}]. Each '
            'item is {"inputs": <body-object>, "route"?: "<route>"} (route defaults to this '
            "requirement's own endpoint). Use the SAME identifiers the main inputs reference so "
            "the entity exists. Empty when the call needs no pre-existing state."
        ),
    )


class FeatureTests(BaseModel):
    feature_id: str = Field(description="Feature these cases belong to, e.g. '2.2'")
    cases: list[TestCase] = Field(default_factory=list)
    pytest_source: str = Field(
        default="",
        description="Runnable pytest module using inputs_json/expected_json from cases",
    )


class GeneratedTests(BaseModel):
    features: list[FeatureTests] = Field(default_factory=list)
