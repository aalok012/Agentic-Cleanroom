include "Replay.dfy"

module F3_2_REQ_9Domain refines Domain {
  type Model = map<string, bool>

  datatype Action = AddClient(client: string) | RemoveClient(client: string)

  ghost predicate Inv(m: Model) {
    true
  }

  function Init(): Model {
    map[]
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case AddClient(client) => m[client := true]
    case RemoveClient(client) => m - {client}
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

  lemma AddClientEnsures(m: Model, client: string)
    ensures (Apply(m, AddClient(client)))[client] == true
  {
  }

  lemma RemoveClientEnsures(m: Model, client: string)
    ensures (client !in Apply(m, RemoveClient(client)))
  {
  }
}

module F3_2_REQ_9Kernel refines Kernel {
  import D = F3_2_REQ_9Domain
}