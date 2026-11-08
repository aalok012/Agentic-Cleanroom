include "Replay.dfy"

module F3_2_REQ_2Domain refines Domain {
  type Model = (map<string, set<string>>, set<string>)

  datatype Action = Register(user: string, event: string)

  ghost predicate Inv(m: Model) {
    var (registrations, confirmed) := m;
    forall u | u in confirmed :: 
      exists e | e in registrations[u] :: true
  }

  function Init(): Model {
    (map[], set[])
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case Register(user, event) =>
      var (registrations, confirmed) := m;
      var newRegs := registrations[user := registrations[user] + {event}];
      var newConfirmed := confirmed + {user};
      (newRegs, newConfirmed)
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

  lemma RegisterEnsuresRegistrationRecorded(user: string, event: string)
    ensures var r := Apply(Init(), Register(user, event)); user in r.0 && event in r.0[user]
  {
  }
}

module F3_2_REQ_2Kernel refines Kernel {
  import D = F3_2_REQ_2Domain
}