include "Replay.dfy"

module F3_2_REQ_8Domain refines Domain {
  type Model = map<string, bool>

  datatype Action = GrantAccess(clientId: string)

  ghost predicate Inv(m: Model) {
    forall k | k in m :: m[k] == true
  }

  function Init(): Model {
    map[]
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case GrantAccess(clientId) => m[clientId := true]
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

  lemma GrantAccessProvidesAccess(clientId: string)
    ensures (clientId in Apply(Init(), GrantAccess(clientId))) && Apply(Init(), GrantAccess(clientId))[clientId] == true
  {
  }
}

module F3_2_REQ_8Kernel refines Kernel {
  import D = F3_2_REQ_8Domain
}