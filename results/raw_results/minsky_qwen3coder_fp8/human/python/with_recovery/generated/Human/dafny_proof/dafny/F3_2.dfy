include "Replay.dfy"

module F3_2Domain refines Domain {
  type Model = (bool, map<string, string>)

  datatype Action = RegisterForEvent(eventId: string)

  ghost predicate Inv(m: Model) {
    true
  }

  function Init(): Model {
    (false, map[])
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case RegisterForEvent(eventId) =>
      if m.0 then
        (m.0, m.1)
      else
        (m.0, m.1)
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

  lemma RegisterForEventRequiresAuth(m: Model, eventId: string)
    requires !m.0
    ensures (Normalize(Apply(m, RegisterForEvent(eventId))).0 == false)
  {
  }
}

module F3_2Kernel refines Kernel {
  import D = F3_2Domain
}