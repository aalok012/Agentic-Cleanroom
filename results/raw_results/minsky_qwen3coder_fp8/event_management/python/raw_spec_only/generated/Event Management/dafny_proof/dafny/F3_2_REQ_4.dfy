include "Replay.dfy"

module F3_2_REQ_4Domain refines Domain {
  type Model = map<string, string>

  datatype Action = PostEvent(eventId: string, eventName: string)

  ghost predicate Inv(m: Model) {
    true
  }

  function Init(): Model {
    map[]
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case PostEvent(eventId, eventName) => m[eventId := eventName]
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

  lemma PostEventEnsures(m: Model, eventId: string, eventName: string)
    ensures (Apply(m, PostEvent(eventId, eventName)))[eventId] == eventName
  {
  }
}

module F3_2_REQ_4Kernel refines Kernel {
  import D = F3_2_REQ_4Domain
}