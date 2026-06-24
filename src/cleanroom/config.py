"""Central run configuration — every pipeline knob, populated from the CLI.

One object threaded through `run()` so each stage can pick its own model, the target language,
pass@k, etc. Defaults preserve today's behavior (all stages on `DEFAULT_MODEL`, proof on
`DAFNY_MODEL`, language=python). See `RunConfig.from_args` for the CLI mapping.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from src.cleanroom.utils.llm_client import DAFNY_MODEL, DEFAULT_MODEL

LANGUAGES = ("python", "java")


@dataclass
class RunConfig:
    # --- target ---
    language: str = "python"          # python | java  (the top-level axis the user picks)
    stack: str = "auto"               # python sub-stack: auto | python | fastapi (ignored for java)

    # --- per-stage models (each stage can run a different model) ---
    spec_model: str = DEFAULT_MODEL
    dependency_model: str = DEFAULT_MODEL
    planning_model: str = DEFAULT_MODEL
    code_model: str = DEFAULT_MODEL
    test_model: str = DEFAULT_MODEL
    proof_model: str = DAFNY_MODEL
    cert_model: str = DEFAULT_MODEL

    # --- certification / proof ---
    certify: bool = False
    samples: int = 1
    k_values: tuple[int, ...] = (1,)
    prove: bool = False
    prove_target: str = "py"
    max_cert_loops: int = 2

    def models_used(self) -> dict[str, str]:
        """Stage -> model, for the run report / debugging."""
        return {
            "spec": self.spec_model, "dependency": self.dependency_model,
            "planning": self.planning_model, "code": self.code_model,
            "test": self.test_model, "proof": self.proof_model, "cert": self.cert_model,
        }

    def as_dict(self) -> dict:
        return {
            "language": self.language, "stack": self.stack, "models": self.models_used(),
            "certify": self.certify, "samples": self.samples, "k_values": list(self.k_values),
            "prove": self.prove, "prove_target": self.prove_target,
            "max_cert_loops": self.max_cert_loops,
        }

    @classmethod
    def from_args(cls, args) -> "RunConfig":
        """Build from an argparse Namespace. Java fixes its own stack; --proof-target follows
        the language (java proves to java) unless the user overrode it."""
        language = getattr(args, "language", "python")
        prove_target = getattr(args, "prove_target", None) or ("java" if language == "java" else "py")
        k_values = tuple(getattr(args, "k", None) or (1,))
        return cls(
            language=language,
            stack="java" if language == "java" else getattr(args, "stack", "auto"),
            spec_model=getattr(args, "spec_model", DEFAULT_MODEL),
            dependency_model=getattr(args, "dependency_model", DEFAULT_MODEL),
            planning_model=getattr(args, "planning_model", DEFAULT_MODEL),
            code_model=getattr(args, "code_model", DEFAULT_MODEL),
            test_model=getattr(args, "test_model", DEFAULT_MODEL),
            proof_model=getattr(args, "proof_model", DAFNY_MODEL),
            cert_model=getattr(args, "cert_model", DEFAULT_MODEL),
            certify=getattr(args, "certify", False),
            samples=getattr(args, "samples", 1),
            k_values=k_values,
            prove=getattr(args, "prove", False),
            prove_target=prove_target,
            max_cert_loops=getattr(args, "max_cert_loops", 2),
        )
