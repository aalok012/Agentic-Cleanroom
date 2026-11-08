include "Replay.dfy"

module F3_1_REQ_2Domain refines Domain {
  type Model = map<string, string>

  datatype Action = UpdateSites

  ghost predicate Inv(m: Model) {
    true
  }

  function Init(): Model {
    map[]
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case UpdateSites => m
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

  lemma UpdateSitesPreservesState(m: Model)
    ensures Apply(m, UpdateSites) == m
  {
  }
}

module F3_1_REQ_2Kernel refines Kernel {
  import D = F3_1_REQ_2Domain
}