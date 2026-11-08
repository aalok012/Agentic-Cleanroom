include "Replay.dfy"

module F3_1_REQ_2Domain refines Domain {
  type Model = map<string, int>

  datatype Action = UpdateDB

  ghost predicate Inv(m: Model) {
    forall k | k in m :: m[k] >= 0
  }

  function Init(): Model {
    map[]
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case UpdateDB => UpdateDatabase(m)
  }

  function UpdateDatabase(m: Model): Model {
    m
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

  lemma UpdateDBPreservesState(m: Model)
    ensures Apply(m, UpdateDB) == m
  {
  }
}

module F3_1_REQ_2Kernel refines Kernel {
  import D = F3_1_REQ_2Domain
}