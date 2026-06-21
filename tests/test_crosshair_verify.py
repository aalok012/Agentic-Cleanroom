"""CrossHair deterministic verification: it flags contract-violating pure functions,
passes correct ones, abstracts counterexamples to spec level, and is skipped on fastapi."""

import pytest

from src.cleanroom.agents.code.schema.code import GeneratedCode, GeneratedFile
from src.cleanroom.agents.verification.crosshair_verify import (
    _abstract,
    _inject_contract,
    _return_type,
    _type_postcondition,
    crosshair_available,
    crosshair_verdicts,
)

requires_crosshair = pytest.mark.skipif(
    not crosshair_available(), reason="crosshair/z3 not available in this environment"
)


def test_return_type_and_postcondition_synthesis():
    assert _return_type("def f(x: int) -> list[dict[str, int]]:") == "list[dict[str, int]]"
    assert _type_postcondition("list[dict]") == "isinstance(__return__, list)"
    assert _type_postcondition("dict") == "isinstance(__return__, dict)"
    assert _type_postcondition("None") == "__return__ is None"
    assert _type_postcondition("SomeCustomType") is None  # cannot synthesize -> fall back


def test_inject_contract_extends_existing_docstring():
    src = 'def f(x: int) -> int:\n    """Doc."""\n    return x\n'
    out = _inject_contract(src, "f", "isinstance(__return__, int)", allow_value_error=True)
    assert "post: isinstance(__return__, int)" in out
    assert "raises: ValueError" in out
    # Body is untouched — CrossHair checks exactly the generated code.
    assert "return x" in out


def test_abstract_never_leaks_concrete_inputs():
    type_v = _abstract("false", "list")
    assert type_v.contract_clause == "postcondition"
    assert "wrong type" in type_v.observation and "(" not in type_v.observation

    crash_v = _abstract("KeyError: 'x'", "dict")
    assert crash_v.contract_clause == "response"
    assert "KeyError" in crash_v.observation
    # No concrete counterexample value leaks through.
    assert "'x'" not in crash_v.observation


def _code(content: str) -> GeneratedCode:
    return GeneratedCode(files=[GeneratedFile(
        fr_id="1.1.REQ-1", feature_id="1.1", path="models/f.py", mvc_layer="model", content=content,
    )])


def _ir(stack: str = "python") -> dict:
    return {
        "stack": stack,
        "planning": {"contracts": [{
            "fr_id": "1.1.REQ-1", "feature_id": "1.1",
            "signature": "def f(x: int) -> list:", "error_mode": "raise",
        }]},
    }


def test_skipped_on_fastapi_stack():
    assert crosshair_verdicts(_ir(stack="fastapi"), _code("def f(x): return [x]")) == {}


@requires_crosshair
def test_flags_wrong_return_type():
    # Returns None (not a list) on a reachable path -> postcondition counterexample.
    code = _code('def f(x: int) -> list:\n    """Doc."""\n    if x == 0:\n        return None\n    return [x]\n')
    verdicts = crosshair_verdicts(_ir(), code, per_condition_timeout=5.0)
    assert verdicts["1.1.REQ-1"].verdict == "fail"
    assert any(v.contract_clause == "postcondition" for v in verdicts["1.1.REQ-1"].violations)


@requires_crosshair
def test_passes_correct_function():
    code = _code('def f(x: int) -> list:\n    """Doc."""\n    return [x]\n')
    verdicts = crosshair_verdicts(_ir(), code, per_condition_timeout=5.0)
    assert verdicts["1.1.REQ-1"].verdict == "pass"
