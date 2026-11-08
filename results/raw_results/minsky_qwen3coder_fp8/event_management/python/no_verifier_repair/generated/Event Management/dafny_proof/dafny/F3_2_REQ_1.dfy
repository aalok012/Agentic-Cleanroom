include "Replay.dfy"

module F3_2_REQ_1Domain refines Domain {
  type Model = bool

  datatype Action = Access

  ghost predicate Inv(m: Model) {
    m
  }

  function Init(): Model {
    true
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case Access => m
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

  lemma AccessPreservesAccessibility(m: Model)
    ensures Apply(m, Access) == m
  {
  }
}

module F3_2_REQ_1Kernel refines Kernel {
  import D = F3_2_REQ_1Domain
}