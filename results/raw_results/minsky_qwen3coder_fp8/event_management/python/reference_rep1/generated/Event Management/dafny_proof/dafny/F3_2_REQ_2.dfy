include "Replay.dfy"

module F3_2_REQ_2Domain refines Domain {
  type Model = map<string, set<string>>

  datatype Action = Register(user: string, event: string)

  ghost predicate Inv(m: Model) {
    forall u | u in m :: 
      forall e | e in m[u] :: 
        e != ""
  }

  function Init(): Model {
    map[]
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case Register(user, event) =>
      if user in m && event !in m[user] then
        m[user := m[user] + {event}]
      else
        m
  }

  function Normalize(m: Model): Model {
    map u | u in m :: 
      set e | e in m[u] :: e
  }

  lemma InitSatisfiesInv()
    ensures Inv(Init())
  {
  }

  lemma StepPreservesInv(m: Model, a: Action)
    ensures Inv(Normalize(Apply(m, a)))
  {
  }

  lemma RegisterRecordsRegistration(m: Model, user: string, event: string)
    requires Inv(m)
    requires user in m && event !in m[user]
    ensures Inv(Apply(m, Register(user, event)))
    ensures user in Apply(m, Register(user, event)) && event in Apply(m, Register(user, event))[user]
  {
    assert Inv(Apply(m, Register(user, event)));
    assert user in Apply(m, Register(user, event));
    assert event in Apply(m, Register(user, event))[user];
  }
}

module F3_2_REQ_2Kernel refines Kernel {
  import D = F3_2_REQ_2Domain
}