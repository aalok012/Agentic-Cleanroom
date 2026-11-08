include "Replay.dfy"

module F3_1Domain refines Domain {
  datatype Event = Event(eventId: string, details: string, registrationRequirements: string)

  type Model = Event

  datatype Action = EditEventDetails(eventId: string, newDetails: string, newRegistrationRequirements: string)

  ghost predicate Inv(m: Model) {
    m.eventId != "" && m.details != "" && m.registrationRequirements != ""
  }

  function Init(): Model {
    Event("", "", "")
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case EditEventDetails(eventId, newDetails, newRegistrationRequirements) =>
      if m.eventId == eventId then
        Event(eventId, newDetails, newRegistrationRequirements)
      else
        m
  }

  function Normalize(m: Model): Model {
    if m.eventId == "" || m.details == "" || m.registrationRequirements == "" then
      Event("", "", "")
    else
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

  lemma EditEventDetailsPreservesInv(eventId: string, newDetails: string, newRegistrationRequirements: string)
    ensures Inv(Normalize(Apply(Event(eventId, newDetails, newRegistrationRequirements), EditEventDetails(eventId, newDetails, newRegistrationRequirements))))
  {
  }
}

module F3_1Kernel refines Kernel {
  import D = F3_1Domain
}