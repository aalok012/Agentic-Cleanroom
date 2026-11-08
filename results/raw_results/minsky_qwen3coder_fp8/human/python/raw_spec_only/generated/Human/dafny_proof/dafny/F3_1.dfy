include "Replay.dfy"

module F3_1Domain refines Domain {
  type Model = map<string, string>

  datatype Action = EditEventDetails(eventId: string, newDetails: string)

  ghost predicate Inv(m: Model) {
    forall k | k in m :: k != ""
  }

  function Init(): Model {
    map[]
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case EditEventDetails(eventId, newDetails) =>
      m[eventId := newDetails]
  }

  function Normalize(m: Model): Model {
    m
  }

  lemma InitSatisfiesInv()
    ensures Inv(Init())
  {
    assert forall k | k in Init() :: k != "";
  }

  lemma StepPreservesInv(m: Model, a: Action)
    ensures Inv(Normalize(Apply(m, a)))
  {
    var result := Apply(m, a);
    assert forall k | k in result :: k != "";
  }

  lemma EditEventDetailsPreservesInv(m: Model, eventId: string, newDetails: string)
    ensures Inv(m[eventId := newDetails])
  {
    assert forall k | k in m[eventId := newDetails] :: k != "";
  }
}

module F3_1Kernel refines Kernel {
  import D = F3_1Domain
}