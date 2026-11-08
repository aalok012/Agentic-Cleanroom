include "Replay.dfy"

module F3_2_REQ_7Domain refines Domain {
  type Model = (int, int)

  datatype Action = NextStep

  ghost predicate Inv(m: Model) {
    var (current, total) := m;
    0 <= current && current <= total
  }

  function Init(): Model {
    (0, 10)
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case NextStep => 
      var (current, total) := m;
      (current + 1, total)
  }

  function Normalize(m: Model): Model {
    var (current, total) := m;
    if current > total then (total, total) else (current, total)
  }

  lemma InitSatisfiesInv()
    ensures Inv(Init())
  {
    assert Inv((0, 10));
  }

  lemma StepPreservesInv(m: Model, a: Action)
    ensures Inv(Normalize(Apply(m, a)))
  {
    var (current, total) := m;
    match a
    case NextStep =>
      assert Inv((current + 1, total));
      assert Inv(Normalize((current + 1, total)));
  }

  lemma NextStepProgresses(m: Model, a: Action)
    requires Inv(m)
    ensures var (newCurrent, _) := Normalize(Apply(m, a)); 
            var (oldCurrent, _) := m; 
            newCurrent >= oldCurrent
  {
  }
}

module F3_2_REQ_7Kernel refines Kernel {
  import D = F3_2_REQ_7Domain
}