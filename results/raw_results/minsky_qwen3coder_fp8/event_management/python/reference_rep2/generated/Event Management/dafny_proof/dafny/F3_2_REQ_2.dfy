include "Replay.dfy"

module F3_2_REQ_2Domain refines Domain {
  type Model = (map<string, set<string>>, set<string>)

  datatype Action = Register(user: string, event: string)

  ghost predicate Inv(m: Model) {
    var (registrations, participants) := m;
    forall u | u in participants :: 
      exists e | e in registrations[u] :: true
  }

  function Init(): Model {
    (map[], set[])
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case Register(user, event) =>
      var (registrations, participants) := m;
      var newRegistrations := registrations[user := registrations[user] + {event}];
      var newParticipants := participants + {user};
      (newRegistrations, newParticipants)
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

  lemma RegisterEnsuresRegistrationRecorded(user: string, event: string, m: Model)
    ensures var (registrations, participants) := Apply(m, Register(user, event));
           user in participants &&
           event in registrations[user]
  {
  }
}

module F3_2_REQ_2Kernel refines Kernel {
  import D = F3_2_REQ_2Domain
}