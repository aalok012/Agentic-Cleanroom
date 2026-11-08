include "Replay.dfy"

module F3_2Domain refines Domain {
  type Model = (bool, set<string>)

  datatype Action = RegisterForEvent(eventId: string)

  ghost predicate Inv(m: Model) {
    true
  }

  function Init(): Model {
    (false, {})
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case RegisterForEvent(eventId) =>
      if m.0 then
        (true, m.1 + {eventId})
      else
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

  lemma RegisterForEventRequiresAuth(m: Model, eventId: string)
    requires m.0 == false
    ensures Apply(m, RegisterForEvent(eventId)) == m
  {
  }
}

module F3_2Kernel refines Kernel {
  import D = F3_2Domain
}