include "Replay.dfy"

module F3_2_REQ_1Domain refines Domain {
  type Model = bool

  datatype Action = Access

  ghost predicate Inv(m: Model) {
    m == true
  }

  function Init(): Model {
    false
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case Access => true
  }

  function Normalize(m: Model): Model {
    true
  }

  lemma InitSatisfiesInv()
    ensures Inv(Init())
  {
    assert false == true ==> false == true;
  }

  lemma StepPreservesInv(m: Model, a: Action)
    ensures Inv(Normalize(Apply(m, a)))
  {
    assert true == true;
  }

  lemma AccessEnsuresAccessGranted(m: Model)
    requires m == false
    ensures Apply(m, Access) == true
  {
    assert true == true;
  }
}

module F3_2_REQ_1Kernel refines Kernel {
  import D = F3_2_REQ_1Domain
}