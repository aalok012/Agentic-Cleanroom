include "Replay.dfy"

module F3_2_REQ_9Domain refines Domain {
  type Model = map<string, bool>

  datatype Action = AddClient(id: string) | DeleteClient(id: string)

  ghost predicate Inv(m: Model) {
    true
  }

  function Init(): Model {
    map[]
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case AddClient(id) => m[id := true]
    case DeleteClient(id) => if id in m then m - {id} else m
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

  lemma AddClientEnsures(m: Model, id: string)
    ensures (Apply(m, AddClient(id)))[id] == true
  {
  }
}

module F3_2_REQ_9Kernel refines Kernel {
  import D = F3_2_REQ_9Domain
}