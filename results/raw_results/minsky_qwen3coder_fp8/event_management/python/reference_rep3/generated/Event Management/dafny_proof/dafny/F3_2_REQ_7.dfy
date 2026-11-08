include "Replay.dfy"

module F3_2_REQ_7Domain refines Domain {
  type Model = int

  datatype Action = NextStep

  ghost predicate Inv(m: Model) {
    m >= 0
  }

  function Init(): Model {
    0
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case NextStep => m + 1
  }

  function Normalize(m: Model): Model {
    if m < 0 then 0 else m
  }

  lemma InitSatisfiesInv()
    ensures Inv(Init())
  {
    assert Inv(0);
  }

  lemma StepPreservesInv(m: Model, a: Action)
    ensures Inv(Normalize(Apply(m, a)))
  {
    assert m >= 0;
    assert Apply(m, a) == m + 1;
    assert Normalize(Apply(m, a)) == m + 1;
    assert m + 1 >= 0;
  }

  lemma NextStepProgresses(m: Model)
    ensures Apply(m, NextStep) == m + 1
  {
  }
}

module F3_2_REQ_7Kernel refines Kernel {
  import D = F3_2_REQ_7Domain
}