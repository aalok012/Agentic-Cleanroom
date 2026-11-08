include "Replay.dfy"

module F3_2Domain refines Domain {
  type Model = (bool, map<string, string>)

  datatype Action = Login(username: string) | Register(event: string)

  ghost predicate Inv(m: Model) {
    let (authenticated, _) = m;
    authenticated ==> |m.1| > 0
  }

  function Init(): Model {
    (false, map[])
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case Login(username) => (true, m.1 + [username := "authenticated"])
    case Register(event) =>
      if m.0 then
        (true, m.1)
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

  lemma RegisterWithoutAuthRedirectsToLogin(m: Model, event: string)
    requires !m.0
    ensures Apply(m, Register(event)) == m
  {
  }
}

module F3_2Kernel refines Kernel {
  import D = F3_2Domain
}