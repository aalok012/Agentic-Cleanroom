include "Replay.dfy"

module F3_2_REQ_11Domain refines Domain {
  type Model = map<int, string>

  datatype Action = GetEvents

  ghost predicate Inv(m: Model) {
    true
  }

  function Init(): Model {
    map[]
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case GetEvents => m
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

  lemma GetEventsReturnsAllEvents(m: Model)
    ensures (forall k | k in Apply(m, GetEvents) :: k in m && Apply(m, GetEvents)[k] == m[k])
  {
  }
}

module F3_2_REQ_11Kernel refines Kernel {
  import D = F3_2_REQ_11Domain
}