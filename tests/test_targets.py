"""Language targets — registry, Python parity, and the Java target (packaging + compile oracle)."""

from pathlib import Path

import pytest

from src.cleanroom.targets import JavaTarget, LanguageTarget, get_target
from src.cleanroom.utils.java_packager import java_class_name, write_java_sources
from src.cleanroom.utils.java_tooling import java_available
from src.cleanroom.utils.prompt_renderer import PromptRenderer


# --- registry + template selection -------------------------------------------
def test_registry_returns_targets():
    assert isinstance(get_target("python"), LanguageTarget)
    assert isinstance(get_target("java"), JavaTarget)
    assert get_target("unknown").language == "python"        # safe fallback


def test_python_target_keeps_existing_templates():
    t = get_target("python")
    assert t.code_template() == "generate_code.j2"
    assert t.test_template() == "generate_tests.j2"
    assert t.oracle_name("fastapi") == "http" and t.oracle_name("python") == "executable"


def test_java_target_templates_and_oracle_name():
    t = get_target("java")
    assert t.code_template() == "generate_code_java.j2"
    assert t.test_template() == "generate_tests_junit.j2"
    assert t.oracle_name("java") == "java" and t.file_ext == ".java"


# --- the Java prompts render (catch template syntax errors offline) -----------
def test_java_prompts_render():
    r = PromptRenderer()
    code = r.render("generate_code_java.j2", {
        "fr_id": "4.1.1", "feature_id": "4.1", "mvc_layer": "controller",
        "signature": "def place_order(name: str) -> dict:", "docstring": "Place an order.",
        "requirement": "Place an order", "prerequisites": [],
        "example_inputs_json": '{"name": "x"}', "expected_return_json": '{"ok": true}',
        "error_mode": "raise", "failure_inputs_json": "",
    })
    assert "public class" in code and "javac" in code            # Java instructions present
    tests = r.render("generate_tests_junit.j2", {
        "feature_id": "4.1", "name": "Place Order", "description": "d",
        "requirements": [{
            "id": "4.1.1", "text": "place an order",
            "signature": "def place_order(name): ...", "stimulus": "place", "precondition": "none",
            "response": "created", "postcondition": "exists", "example_inputs_json": '{"name": "x"}',
            "expected_return_json": '{"ok": true}', "failure_inputs_json": "", "error_mode": "raise",
        }],
    })
    assert "JUnit5" in tests and "assertThrows" in tests


# --- java packaging -----------------------------------------------------------
def test_java_class_name_extraction():
    assert java_class_name("public class Menu {}", "X") == "Menu"
    assert java_class_name("public final class Order {}", "X") == "Order"
    assert java_class_name("// no class here", "Fallback") == "Fallback"


def test_write_java_sources_names_files_by_public_class(tmp_path):
    gen = {"files": [
        {"fr_id": "4.1.1", "content": "public class PlaceOrder { }"},
        {"fr_id": "4.2.1", "content": "import java.util.*;\npublic class CancelOrder { }"},
    ]}
    written = write_java_sources(gen, tmp_path)
    names = sorted(p.name for p in written)
    assert names == ["CancelOrder.java", "PlaceOrder.java"]
    assert (tmp_path / "src" / "PlaceOrder.java").exists()


# --- java compile oracle (skips cleanly without a JDK) ------------------------
@pytest.mark.skipif(not java_available(), reason="no javac on PATH")
def test_run_case_java_compiles_valid_and_rejects_broken(tmp_path):
    from src.cleanroom.agents.evaluation.runner import run_case_java

    good = tmp_path / "good"
    write_java_sources({"files": [{"fr_id": "1", "content": "public class Ok { public int f(){ return 1; } }"}]}, good)
    ok, reason = run_case_java(good, {}, {}, timeout=60)
    assert ok, reason

    bad = tmp_path / "bad"
    write_java_sources({"files": [{"fr_id": "1", "content": "public class Bad { this won't compile }"}]}, bad)
    ok, reason = run_case_java(bad, {}, {}, timeout=60)
    assert not ok and "javac" in reason


def test_java_oracle_unavailable_is_graceful(monkeypatch):
    """When javac is absent the Java target reports oracle unavailable (run skips, not crashes)."""
    import src.cleanroom.utils.java_tooling as jt
    monkeypatch.setattr(jt, "javac_path", lambda: None)
    assert get_target("java").oracle_available() is False
