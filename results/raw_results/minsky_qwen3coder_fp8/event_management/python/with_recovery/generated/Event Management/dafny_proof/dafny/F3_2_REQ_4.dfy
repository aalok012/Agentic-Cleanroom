include "Replay.dfy"

module F3_2_REQ_4Domain refines Domain {
  type Model = map<string, string>

  datatype Action = PostEvent(eventId: string, content: string)

  ghost predicate Inv(m: Model) {
    forall k | k in m :: k != ""
  }

  function Init(): Model {
    map[]
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case PostEvent(eventId, content) => m[eventId := content]
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
    assert forall k | k in Normalize(Apply(m, a)) :: k != "";
  }

  lemma PostEventEnsuresStudentCanViewAndRegister(m: Model, eventId: string, content: string)
    ensures (Normalize(Apply(m, PostEvent(eventId, content)))[eventId] == content)
  {
    var newModel := Apply(m, PostEvent(eventId, content));
    assert eventId in newModel;
    assert newModel[eventId] == content;
    assert Normalize(newModel)[eventId] == content;
  }
}

module F3_2_REQ_4Kernel refines Kernel {
  import D = F3_2_REQ_4Domain
}