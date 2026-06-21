"""DafnyAgent generate/verify/revise loop, offline (fake LLM + real Dafny verifier).

Skipped unless both the scaffolded LemmaFit project and the Dafny toolchain are present."""

from types import SimpleNamespace

import pytest

from src.cleanroom.agents.dafny.agent import DafnyAgent
from src.cleanroom.utils.dafny_verify import dafny_available
from src.cleanroom.utils.lemmafit_project import lemmafit_available, scaffold_lemmafit_project

requires_env = pytest.mark.skipif(
    not (dafny_available() and lemmafit_available()),
    reason="needs the lemmafit CLI + dafny toolchain",
)


@pytest.fixture(scope="module")
def project(tmp_path_factory):
    """A throwaway scaffolded LemmaFit project (no npm install — only the verifier is needed)."""
    if not (dafny_available() and lemmafit_available()):
        pytest.skip("needs the lemmafit CLI + dafny toolchain")
    return scaffold_lemmafit_project(tmp_path_factory.mktemp("lf") / "proj", install_deps=False)

# A minimal module that refines the abstract Domain and verifies.
_GOOD = '''include "Replay.dfy"
module TDomain refines Domain {
  type Model = int
  datatype Action = Noop
  ghost predicate Inv(m: Model) { m >= 0 }
  function Init(): Model { 0 }
  function Apply(m: Model, a: Action): Model { m }
  function Normalize(m: Model): Model { if m < 0 then 0 else m }
  lemma InitSatisfiesInv() ensures Inv(Init()) {}
  lemma StepPreservesInv(m: Model, a: Action) ensures Inv(Normalize(Apply(m, a))) {}
}
module TKernel refines Kernel { import D = TDomain }
'''

# Same, but with a proof that fails — forces a revise round.
_BAD = _GOOD.replace("ensures Inv(Init()) {}", "ensures Inv(Init()) { assert false; }")


class FakeLLM:
    """Returns canned Dafny per call (last response repeats)."""

    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = 0

    def invoke(self, _messages):
        r = self.responses[min(self.calls, len(self.responses) - 1)]
        self.calls += 1
        return SimpleNamespace(content=r)


def _ir() -> dict:
    return {
        "features": [{"id": "9.9", "name": "Spike Feature"}],
        "planning": {"contracts": [{
            "fr_id": "9.9.REQ-1", "feature_id": "9.9", "prerequisite_fr_ids": [],
            "contract": {"stimulus": "noop", "precondition": "none",
                         "response": "state unchanged", "postcondition": "value stays non-negative"},
        }]},
    }


@requires_env
def test_verifies_first_round(project):
    agent = DafnyAgent(project, llm=FakeLLM([_GOOD]), max_rounds=5)
    res = agent.generate_feature(_ir(), "9.9")
    assert res.verified and res.rounds == 1
    assert res.module == "F9_9"
    (agent.dafny_dir / "F9_9.dfy").unlink(missing_ok=True)


@requires_env
def test_revises_until_verified(project):
    agent = DafnyAgent(project, llm=FakeLLM([_BAD, _GOOD]), max_rounds=5)
    res = agent.generate_feature(_ir(), "9.9")
    assert res.verified and res.rounds == 2          # failed round 1, fixed round 2
    (agent.dafny_dir / "F9_9.dfy").unlink(missing_ok=True)


@requires_env
def test_reports_unverified_after_budget(project):
    agent = DafnyAgent(project, llm=FakeLLM([_BAD]), max_rounds=2)
    res = agent.generate_feature(_ir(), "9.9")
    assert not res.verified and res.rounds == 2 and res.residual_errors
    (agent.dafny_dir / "F9_9.dfy").unlink(missing_ok=True)
