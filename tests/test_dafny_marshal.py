"""Marshalling shim between JSON/DB primitives and Dafny's Python runtime types.

The authoritative test is `test_roundtrip_through_real_compiled_core`: it compiles a real Dafny
state machine, then drives the PROVED core through the shim exactly as a FastAPI adapter would —
this is what proves the 'ship the Dafny core + thin glue' design actually runs. A tiny fake-runtime
unit test covers the str conversions without needing the toolchain.
"""

import sys
from types import SimpleNamespace

import pytest

from src.cleanroom.utils import dafny_marshal
from src.cleanroom.utils.dafny_verify import dafny_available


# --- unit: str conversions against a faithful fake `_dafny` -----------------------
class _FakeSeq:
    def __init__(self, s): self._s = s
    def VerbatimString(self, _verbatim): return self._s


def test_str_conversions_use_runtime(monkeypatch):
    monkeypatch.setattr(dafny_marshal, "_rt", lambda: SimpleNamespace(Seq=_FakeSeq))
    wrapped = dafny_marshal.to_str("Pizza")
    assert isinstance(wrapped, _FakeSeq)
    assert dafny_marshal.from_str(wrapped) == "Pizza"


# --- integration: drive a real compiled Dafny core through the shim ----------------
_MENU = '''include "Replay.dfy"
module FmDomain refines Domain {
  type Model = map<string, int>
  datatype Action = Add(name: string, price: int) | Remove(name: string)
  ghost predicate Inv(m: Model) { forall k | k in m :: m[k] >= 0 }
  function Init(): Model { map[] }
  function Apply(m: Model, a: Action): Model {
    match a
    case Add(name, price) => m[name := price]
    case Remove(name)     => m - {name}
  }
  function Normalize(m: Model): Model { map k | k in m && m[k] >= 0 :: m[k] }
  lemma InitSatisfiesInv() ensures Inv(Init()) {}
  lemma StepPreservesInv(m: Model, a: Action) ensures Inv(Normalize(Apply(m, a))) {}
}
'''


@pytest.mark.skipif(not dafny_available(), reason="needs the dafny toolchain")
def test_roundtrip_through_real_compiled_core(tmp_path):
    from src.cleanroom.utils.dafny_project import scaffold_dafny_project, compile_dafny
    from src.cleanroom.agents.dafny.schema.dafny import FeatureDafny, GeneratedDafny

    proj = scaffold_dafny_project(tmp_path / "proj")
    (proj / "dafny" / "Fm.dfy").write_text(_MENU)
    gen = GeneratedDafny(features=[FeatureDafny(
        feature_id="9.9", module="Fm", dafny_source=_MENU, verified=True)])
    res = compile_dafny(proj, gen, target="py")
    assert res["compiled"], f"compile failed: {res}"

    core_dir = str((proj / "out" / "Fm-py").resolve())
    sys.path.insert(0, core_dir)
    try:
        for m in ("_dafny", "module_", "System_", "FmDomain"):
            sys.modules.pop(m, None)
        import FmDomain  # the compiled, proved logic

        Dom = FmDomain.default__
        step = lambda st, a: Dom.Normalize(Dom.Apply(st, a))

        # Drive it like an adapter would: build Actions from "request" values via the shim.
        state = Dom.Init()
        state = step(state, FmDomain.Action_Add(dafny_marshal.to_str("Pizza"), 10))
        state = step(state, FmDomain.Action_Add(dafny_marshal.to_str("Pasta"), 12))
        state = step(state, FmDomain.Action_Remove(dafny_marshal.to_str("Pizza")))

        # Marshal the proved result back to a JSON-able dict.
        assert dafny_marshal.from_map(state, vconv=int) == {"Pasta": 12}
    finally:
        sys.path.remove(core_dir)
        for m in ("_dafny", "module_", "System_", "FmDomain"):
            sys.modules.pop(m, None)
