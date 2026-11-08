include "Replay.dfy"

module F3_2Domain refines Domain {
  type Model = (bool, set<string>)

  datatype Action = Register(event: string)

  ghost predicate Inv(m: Model) {
    m.0 ==> m.1 == {}
  }

  function Init(): Model {
    (false, {})
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case Register(event) =>
      if m.0 then
        (true, m.1 + {event})
      else
        m
  }

  function Normalize(m: Model): Model {
    if m.0 then m else (false, {})
  }

  lemma InitSatisfiesInv()
    ensures Inv(Init())
  {
    assert (false ==> {} == {}) == true;
  }

  lemma StepPreservesInv(m: Model, a: Action)
    ensures Inv(Normalize(Apply(m, a)))
  {
    assert (Normalize(Apply(m, a))).0 ==> (Normalize(Apply(m, a))).1 == {};
  }

  lemma RegisterRequiresAuth(m: Model, event: string)
    requires m.0 == false
    ensures Apply(m, Register(event)) == m
  {
    assert Apply(m, Register(event)) == m;
  }
}

module F3_2Kernel refines Kernel {
  import D = F3_2Domain
}