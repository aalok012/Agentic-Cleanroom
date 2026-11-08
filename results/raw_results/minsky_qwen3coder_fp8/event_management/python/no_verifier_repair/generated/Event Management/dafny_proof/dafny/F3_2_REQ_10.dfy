include "Replay.dfy"

module F3_2_REQ_10Domain refines Domain {
  type Model = map<string, string>

  datatype Action = AppendEvent(eventId: string, eventData: string)

  ghost predicate Inv(m: Model) {
    true
  }

  function Init(): Model {
    map[]
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case AppendEvent(eventId, eventData) => m[eventId := eventData]
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

  lemma AppendEventEnsuresPersistency(m: Model, eventId: string, eventData: string)
    ensures (Apply(m, AppendEvent(eventId, eventData)))[eventId] == eventData
  {
  }
}

module F3_2_REQ_10Kernel refines Kernel {
  import D = F3_2_REQ_10Domain
}