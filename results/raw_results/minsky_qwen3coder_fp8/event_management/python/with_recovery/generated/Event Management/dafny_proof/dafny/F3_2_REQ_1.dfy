include "Replay.dfy"

module F3_2_REQ_1Domain refines Domain {
  type Model = bool

  datatype Action = Access

  ghost predicate Inv(m: Model) {
    m == true || m == false
  }

  function Init(): Model {
    false
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case Access => true
  }

  function Normalize(m: Model): Model {
    m
  }

  lemma InitSatisfiesInv()
    ensures Inv(Init())
  {
  }

  lemma StepPreservesInv(m: Model, a: Action)
    ensures Inv(Normalize(Apply(m, a)))
  {
  }

  lemma AccessMakesFeatureAccessible(m: Model)
    requires Inv(m)
    ensures Apply(m, Access) == true
  {
  }
}

module F3_2_REQ_1Kernel refines Kernel {
  import D = F3_2_REQ_1Domain
}