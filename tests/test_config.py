"""RunConfig — CLI → config mapping (per-stage models, language→stack, pass@k)."""

from types import SimpleNamespace

from src.cleanroom.config import RunConfig
from src.cleanroom.utils.llm_client import DAFNY_MODEL, DEFAULT_MODEL


def _ns(**kw):
    base = dict(
        language="python", stack="auto",
        spec_model=DEFAULT_MODEL, dependency_model=DEFAULT_MODEL, planning_model=DEFAULT_MODEL,
        code_model=DEFAULT_MODEL, test_model=DEFAULT_MODEL, proof_model=DAFNY_MODEL,
        cert_model=DEFAULT_MODEL, certify=False, samples=1, k=None, prove=False,
        prove_target=None, max_cert_loops=2,
    )
    base.update(kw)
    return SimpleNamespace(**base)


def test_python_defaults():
    cfg = RunConfig.from_args(_ns())
    assert cfg.language == "python" and cfg.stack == "auto"
    assert cfg.prove_target == "py" and cfg.k_values == (1,)
    assert cfg.proof_model == DAFNY_MODEL          # proof keeps the strong model by default


def test_java_fixes_stack_and_prove_target():
    cfg = RunConfig.from_args(_ns(language="java"))
    assert cfg.stack == "java"                     # java pins its own stack regardless of --stack
    assert cfg.prove_target == "java"              # proof target follows the language


def test_prove_target_override_is_respected():
    cfg = RunConfig.from_args(_ns(language="java", prove_target="py"))
    assert cfg.prove_target == "py"


def test_per_stage_models_are_independent():
    cfg = RunConfig.from_args(_ns(code_model="gpt-4.1", test_model="model-x"))
    m = cfg.models_used()
    assert m["code"] == "gpt-4.1" and m["test"] == "model-x"
    assert m["spec"] == DEFAULT_MODEL and m["proof"] == DAFNY_MODEL


def test_k_values_from_cli():
    assert RunConfig.from_args(_ns(k=[1, 3])).k_values == (1, 3)
    assert RunConfig.from_args(_ns(k=None)).k_values == (1,)
