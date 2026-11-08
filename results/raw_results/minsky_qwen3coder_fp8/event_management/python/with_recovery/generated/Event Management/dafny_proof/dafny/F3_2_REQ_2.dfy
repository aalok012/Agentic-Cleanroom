include "Replay.dfy"

module F3_2_REQ_2Domain refines Domain {
  type Model = map<string, set<string>>

  datatype Action = Register(user: string, event: string)

  ghost predicate Inv(m: Model) {
    forall u | u in m.Keys :: forall e | e in m[u] :: e != ""
  }

  function Init(): Model {
    map[]
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case Register(u, e) => m[u := (if u in m then m[u] + {e} else {e})]
  }

  function Normalize(m: Model): Model {
    map u | u in m.Keys :: m[u]
  }

  lemma InitSatisfiesInv()
    ensures Inv(Init())
  {
  }

  lemma StepPreservesInv(m: Model, a: Action)
    ensures Inv(Normalize(Apply(m, a)))
  {
  }

  lemma RegisterRecordsRegistration(u: string, e: string, m: Model)
    ensures (Apply(m, Register(u, e)))[u] == (if u in m then m[u] + {e} else {e})
  {
  }
}

module F3_2_REQ_2Kernel refines Kernel {
  import D = F3_2_REQ_2Domain
}