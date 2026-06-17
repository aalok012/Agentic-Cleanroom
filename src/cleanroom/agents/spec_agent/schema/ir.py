from typing import Literal, Optional

from pydantic import BaseModel, Field

# Fixed NFR taxonomy. The LLM must pick exactly one of these for each NFR.
NFR_CATEGORIES = (
    "performance",
    "robustness",
    "security",
    "availability",
    "maintainability",
    "privacy",
    "usability",
    "other",
)


class FunctionalRequirement(BaseModel):
    """A requirement describing what the system DOES (behavior / input / output)."""

    id: str = Field(description="Section ID exactly as in the SRS, e.g. '2.2.1.1' — assigned by the parser, never the LLM")
    text: str = Field(description="Requirement text copied or closely paraphrased from the SRS")


class NonFunctionalRequirement(BaseModel):
    """A quality attribute / constraint beyond functionality, with a rationale."""

    id: str = Field(description="Section ID exactly as in the SRS — assigned by the parser, never the LLM")
    text: str = Field(description="Requirement text copied or closely paraphrased from the SRS")
    category: str = Field(description="One of: performance, robustness, security, availability, maintainability, privacy, usability, other")
    rationale: str = Field(description="Why this constraint exists / what it protects against, grounded in the requirement and its feature")


class Feature(BaseModel):
    id: str = Field(default="", description="Feature/section ID from the SRS, e.g. '2.2'")
    name: str
    description: str = ""
    functional_requirements: list[FunctionalRequirement] = Field(default_factory=list)
    non_functional_requirements: list[NonFunctionalRequirement] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Per-feature LLM classification result (used with with_structured_output()).
# The LLM only labels requirements; their id and text always come from the parser.
# ---------------------------------------------------------------------------
class RequirementClassification(BaseModel):
    id: str = Field(description="The requirement id, echoed VERBATIM from the input — never changed or invented")
    kind: Literal["FR", "NFR"] = Field(description="FR if it describes behavior; NFR if it is a quality/constraint")
    category: Optional[str] = Field(default=None, description="For NFR only: one of the fixed NFR categories")
    rationale: Optional[str] = Field(default=None, description="For NFR only: why the constraint exists / what it protects against")


class FeatureClassification(BaseModel):
    classifications: list[RequirementClassification] = Field(default_factory=list)


class Specification(BaseModel):
    feature_name: str
    inputs: Optional[list[str]] = Field(default=None, description="ONLY if explicitly stated in the SRS, else null")
    outputs: Optional[list[str]] = Field(default=None, description="ONLY if explicitly stated in the SRS, else null")
    preconditions: Optional[list[str]] = Field(default=None, description="ONLY if explicitly stated in the SRS, else null")
    postconditions: Optional[list[str]] = Field(default=None, description="ONLY if explicitly stated in the SRS, else null")
    side_effects: Optional[list[str]] = Field(default=None, description="ONLY if explicitly stated in the SRS, else null")
    dependencies: Optional[list[str]] = Field(default=None, description="ONLY if explicitly stated in the SRS, else null")


class IntermediateRepresentation(BaseModel):
    project_name: str
    source_file: str
    features: list[Feature] = Field(default_factory=list)
    specifications: list[Specification] = Field(default_factory=list)
    extraction_notes: list[str] = Field(default_factory=list)
