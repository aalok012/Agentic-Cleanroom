include "Replay.dfy"

module F3_2_REQ_6Domain refines Domain {
  type Model = map<string, string>

  datatype Action = StoreCredential(username: string, password: string)

  ghost predicate Inv(m: Model) {
    true
  }

  function Init(): Model {
    map[]
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case StoreCredential(u, p) => m[u := p]
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

  lemma StoreCredentialEnsures(m: Model, u: string, p: string)
    ensures Apply(m, StoreCredential(u, p)) == m[u := p]
  {
  }
}

module F3_2_REQ_6Kernel refines Kernel {
  import D = F3_2_REQ_6Domain
}