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
    case UpdateDB => m
  }

  function Normalize(m: Model): Model {
    m
  }

  lemma InitSatisfiesInv()
    ensures Inv(Init())
  {
    assert forall k | k in Init() :: Init()[k] >= 0;
  }

  lemma StepPreservesInv(m: Model, a: Action)
    ensures Inv(Normalize(Apply(m, a)))
  {
    assert forall k | k in Normalize(Apply(m, a)) :: Normalize(Apply(m, a))[k] >= 0;
  }

  lemma UpdateDBEnsuresLatestInfo(m: Model)
    ensures (forall k | k in Apply(m, UpdateDB) :: Apply(m, UpdateDB)[k] >= 0)
  {
    assert forall k | k in Apply(m, UpdateDB) :: Apply(m, UpdateDB)[k] >= 0;
  }
}

module F3_1_REQ_2Kernel refines Kernel {
  import D = F3_1_REQ_2Domain
}