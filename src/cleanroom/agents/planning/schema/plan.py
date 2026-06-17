from typing import Literal

from pydantic import BaseModel, Field


class Contract(BaseModel):
    """An implementation contract for ONE functional requirement.

    Produced from the SPEC only (no code, no tests). Signature, docstring, and the
    MVC layer come from LLM interpretation; file_path is derived deterministically
    from the layer, and prerequisite_fr_ids come from the FR-level dependency edges.
    """

    fr_id: str = Field(description="Functional requirement id, from the parser — never invented")
    feature_id: str = Field(description="Owning feature id")
    signature: str = Field(description="Concrete function signature: name, typed params, return type")
    docstring: str = Field(description="What the function does + the feature's NFR constraints to satisfy")
    mvc_layer: Literal["model", "view", "controller"] = Field(description="'model' | 'view' | 'controller'")
    file_path: str = Field(description="Deterministic path derived from the MVC layer")
    prerequisite_fr_ids: list[str] = Field(
        default_factory=list, description="FRs (same feature) that must be built first — from fr_edges"
    )


class PlanningOutput(BaseModel):
    contracts: list[Contract] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Per-feature LLM design result (used with with_structured_output()).
# The LLM only designs; ids always come from the parser/dependency stages.
# ---------------------------------------------------------------------------
class ArgDoc(BaseModel):
    """One parameter's documentation, for the docstring's Args section."""

    name: str = Field(description="Parameter name — must match a parameter in the signature exactly")
    description: str = Field(description="What this parameter is and any constraints on it")


class FRPlan(BaseModel):
    id: str = Field(description="The requirement id, echoed VERBATIM from the input — never changed or invented")
    signature: str = Field(description="One-line Python function signature: name, typed params, return type")
    summary: str = Field(description="1-3 sentences describing what the function does, grounded in the requirement")
    args: list[ArgDoc] = Field(
        default_factory=list, description="One entry per signature parameter (omit if the signature takes none)"
    )
    returns: str = Field(default="", description="What the function returns (leave empty for a None return)")
    notes: str = Field(
        default="",
        description=(
            "Edge cases, preconditions, or prerequisite behavior stated in the requirement "
            "(e.g. 'if no specimen record exists, link by Subject ID'). Empty if none."
        ),
    )
    mvc_layer: Literal["model", "view", "controller"] = Field(description="EXACTLY one of: model, view, controller")


class FeaturePlan(BaseModel):
    plans: list[FRPlan] = Field(default_factory=list)