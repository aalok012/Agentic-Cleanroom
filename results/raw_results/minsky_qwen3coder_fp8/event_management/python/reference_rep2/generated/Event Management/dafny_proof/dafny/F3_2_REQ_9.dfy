include "Replay.dfy"

module F3_2_REQ_9Domain refines Domain {
  type Model = map<string, set<string>>

  datatype Action = AddClientAccess(clientId: string, permissions: set<string>)

  ghost predicate Inv(m: Model) {
    true
  }

  function Init(): Model {
    map[]
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case AddClientAccess(clientId, permissions) =>
      if clientId in m then
        m[clientId := m[clientId] + permissions]
      else
        m[clientId := permissions]
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

  lemma AddClientAccessEnsures(m: Model, clientId: string, permissions: set<string>)
    ensures clientId in Apply(m, AddClientAccess(clientId, permissions))
  {
    if clientId in m {
      assert clientId in Apply(m, AddClientAccess(clientId, permissions));
    } else {
      assert clientId in Apply(m, AddClientAccess(clientId, permissions));
    }
  }
}

module F3_2_REQ_9Kernel refines Kernel {
  import D = F3_2_REQ_9Domain
}