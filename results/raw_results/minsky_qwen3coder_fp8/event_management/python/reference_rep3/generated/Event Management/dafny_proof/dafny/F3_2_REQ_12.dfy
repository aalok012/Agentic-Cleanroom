include "Replay.dfy"

module F3_2_REQ_12Domain refines Domain {
  type Model = bool

  datatype Action = None

  ghost predicate Inv(m: Model) {
    true
  }

  function Init(): Model {
    false
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case None => m
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

  lemma NoneActionPreservesState(m: Model)
    ensures Apply(m, None) == m
  {
  }
}

module F3_2_REQ_12Kernel refines Kernel {
  import D = F3_2_REQ_12Domain
}