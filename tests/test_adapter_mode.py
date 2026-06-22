"""CodeAgent adapter mode + Dafny-core staging (the 'ship Dafny core + thin glue' wiring).

Offline: a fake LLM stands in for the adapter author; these lock the deterministic plumbing
(prompt conventions, file placement, feature-skipping, core/shim packaging). Adapter *quality*
is an LLM concern validated on a real --prove run, not here.
"""

import pathlib
from types import SimpleNamespace

from src.cleanroom.agents.code.agent import CodeAgent
from src.cleanroom.utils.dafny_project import stage_dafny_cores


def _ir():
    return {
        "project_name": "demo",
        "features": [
            {"id": "4.1", "name": "Place Order",
             "functional_requirements": [{"id": "4.1.1", "text": "place an order"}]},
            {"id": "4.2", "name": "Cancel Order",
             "functional_requirements": [{"id": "4.2.1", "text": "cancel an order"}]},
        ],
        "planning": {"contracts": [
            {"fr_id": "4.1.1", "feature_id": "4.1", "mvc_layer": "controller",
             "signature": "place_order(name)", "docstring": "d", "file_path": "controllers/place.py",
             "prerequisite_fr_ids": [],
             "contract": {"fr_id": "4.1.1", "feature_id": "4.1", "stimulus": "place",
                          "precondition": "none", "response": "created", "postcondition": "exists"}},
            {"fr_id": "4.2.1", "feature_id": "4.2", "mvc_layer": "controller",
             "signature": "cancel_order(id)", "docstring": "d", "file_path": "controllers/cancel.py",
             "prerequisite_fr_ids": [],
             "contract": {"fr_id": "4.2.1", "feature_id": "4.2", "stimulus": "cancel",
                          "precondition": "exists", "response": "cancelled", "postcondition": "gone"}},
        ]},
    }


class _FakeLLM:
    def __init__(self, capture=None):
        self.capture = capture
    def with_structured_output(self, schema):
        cap = self.capture
        class S:
            def invoke(self, prompt):
                if cap is not None:
                    cap.append(prompt)
                return SimpleNamespace(content="from fastapi import APIRouter\nrouter = APIRouter()\n")
        return S()


def test_generate_adapter_places_file_and_embeds_calling_convention():
    prompts: list = []
    gf = CodeAgent(llm=_FakeLLM(prompts), stack="fastapi").generate_adapter(
        _ir(), "4.1", "F4_1", 'include "Replay.dfy"\nmodule F4_1Domain refines Domain {}')
    assert gf.path == "controllers/f4_1_adapter.py"
    assert gf.mvc_layer == "controller" and gf.feature_id == "4.1"
    p = prompts[0]
    # the proved-core calling convention must be in the prompt
    assert "dafny_marshal" in p and "Normalize(Dom.Apply" in p
    # Dafny mangles `_` -> `__` in compiled module names: F4_1Domain compiles to F4__1Domain.
    # The import name MUST be the mangled one; the core DIR keeps the single underscore.
    assert "F4__1Domain" in p
    assert "F4_1-py" in p


def test_generate_skips_proved_features():
    code = CodeAgent(llm=_FakeLLM(), stack="fastapi").generate(_ir(), skip_feature_ids={"4.1"})
    fids = {f.feature_id for f in code.files}
    assert fids == {"4.2"}          # 4.1 (proved) omitted; 4.2 generated


def test_stage_dafny_cores_copies_core_and_shim(tmp_path):
    proj = tmp_path / "proj"
    (proj / "out" / "F4_1-py").mkdir(parents=True)
    (proj / "out" / "F4_1-py" / "F4_1Domain.py").write_text("# core\n")
    app = tmp_path / "app"
    app.mkdir()
    res = stage_dafny_cores(app, proj, ["F4_1", "F9_9"])
    assert res["staged"] == ["F4_1"] and res["missing"] == ["F9_9"]
    assert (app / "dafny_cores" / "F4_1-py" / "F4_1Domain.py").exists()
    assert (app / "dafny_cores" / "dafny_marshal.py").exists()
