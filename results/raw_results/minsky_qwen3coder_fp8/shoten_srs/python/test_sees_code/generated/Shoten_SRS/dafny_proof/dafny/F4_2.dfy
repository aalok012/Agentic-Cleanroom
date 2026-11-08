include "Replay.dfy"

module F4_2Domain refines Domain {
  type Model = (bool, map<string, string>)

  datatype Action = Login(username: string, password: string)

  ghost predicate Inv(m: Model) {
    m.0 ==> |m.1| > 0
  }

  function Init(): Model {
    (false, map[])
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case Login(username, password) =>
      let (authenticated, credentials) = m;
      if authenticated then m
      else if username in credentials && credentials[username] == password then (true, credentials)
      else m
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

  lemma LoginSucceeds(m: Model, a: Action)
    requires a == Login("alice", "secret")
    ensures (Apply(m, a)).0
  {
  }
}

module F4_2Kernel refines Kernel {
  import D = F4_2Domain
}