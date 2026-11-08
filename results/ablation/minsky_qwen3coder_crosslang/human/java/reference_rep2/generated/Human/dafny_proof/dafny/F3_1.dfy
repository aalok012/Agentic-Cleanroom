include "Replay.dfy"

module F3_1Domain refines Domain {
  datatype Event = Event(title: string, description: string, maxRegistrations: int)

  type Model = Event

  datatype Action = EditEvent

  ghost predicate Inv(m: Model) {
    m.title != "" && m.description != ""
  }

  function Init(): Model {
    Event(title: "", description: "", maxRegistrations: 0)
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case EditEvent => m
  }

  function Normalize(m: Model): Model {
    if m.title == "" then Event("Untitled Event", m.description, m.maxRegistrations) else m
  }

  lemma InitSatisfiesInv()
    ensures Inv(Init())
  {
  }

  lemma StepPreservesInv(m: Model, a: Action)
    ensures Inv(Normalize(Apply(m, a)))
  {
  }

  lemma EditEventUpdatesEvent(m: Model)
    requires m.title != "" && m.description != ""
    ensures Apply(m, EditEvent).title == m.title && Apply(m, EditEvent).description == m.description
  {
  }
}

module F3_1Kernel refines Kernel {
  import D = F3_1Domain
}