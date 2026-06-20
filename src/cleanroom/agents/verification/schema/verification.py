"""Schemas for the Verification Agent — contract-conformance review.

The verifier is a reasoning-only reviewer: it judges whether generated code satisfies its
spec-derived contract, and on failure reports SPEC-LEVEL violations that flow back to the
Code Agent. The shape of these models is the structural guard that keeps the feedback
spec-level: a violation can only name a CONTRACT CLAUSE and describe what the code does
wrong relative to it. There is deliberately NO field for example inputs, expected outputs,
or test cases — so the loop can never leak test-style information into code generation.
"""

from typing import Literal

from pydantic import BaseModel, Field

# The only clauses a violation may reference. Anchoring to contract concepts (not "input"
# or "expected output") is what keeps reviewer feedback at the specification level.
ContractClause = Literal[
    "precondition",
    "stimulus",
    "response",
    "postcondition",
    "signature",
    "prerequisite_call",
    "coverage",
    "canonical_call",
]


class ContractViolation(BaseModel):
    """One way the code under review breaks its contract, named by the clause it violates."""

    contract_clause: ContractClause = Field(
        description="Which clause of the spec-derived contract the code violates"
    )
    observation: str = Field(
        description=(
            "Spec-level description of what the code does wrong relative to that clause "
            "(e.g. 'the postcondition guarantees X but the code returns Y'). NEVER an "
            "example input, an expected output, or a test case."
        )
    )


class ContractVerdict(BaseModel):
    """The verifier's output for ONE contract (fr_id) — the per-call structured-output target."""

    fr_id: str = Field(description="Functional requirement under review")
    verdict: Literal["pass", "fail"] = Field(
        description="Whether the code satisfies the contract for this requirement"
    )
    violations: list[ContractViolation] = Field(
        default_factory=list,
        description="Empty on pass; one entry per contract clause the code breaks",
    )


class VerificationResult(BaseModel):
    """Aggregate verification outcome for one code artifact, stored in ir['verification']."""

    model: str = ""
    max_rounds: int = Field(default=0, description="Cap on revise rounds the loop was allowed")
    rounds_used: int = Field(default=0, description="Revise rounds actually performed")
    verdicts: list[ContractVerdict] = Field(
        default_factory=list, description="Final per-contract verdicts after the loop"
    )
    n_contracts: int = 0
    n_passing: int = Field(default=0, description="Contracts that pass after the loop")
    n_failing: int = 0
    residual_failures: list[str] = Field(
        default_factory=list, description="fr_ids still failing after max_rounds"
    )
    notes: list[str] = Field(default_factory=list)
