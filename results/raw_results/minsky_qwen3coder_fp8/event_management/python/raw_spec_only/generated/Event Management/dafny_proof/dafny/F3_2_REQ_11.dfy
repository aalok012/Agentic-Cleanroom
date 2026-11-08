include "Replay.dfy"

module F3_2_REQ_11Domain refines Domain {
  type Model = map<string, int>

  datatype Action = AddEvent(event: string, timestamp: int)

  ghost predicate Inv(m: Model) {
    true
  }

  function Init(): Model {
    map[]
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case AddEvent(event, timestamp) => m[event := timestamp]
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

  lemma AddEventIncreasesSize(m: Model, event: string, timestamp: int)
    ensures |Normalize(Apply(m, AddEvent(event, timestamp)))| == |m| + 1
  {
  }
}

module F3_2_REQ_11Kernel refines Kernel {
  import D = F3_2_REQ_11Domain
}