include "Replay.dfy"

module F3_2_REQ_6Domain refines Domain {
  type Model = map<string, map<string, string>>

  datatype Action = AddStakeholder(name: string, credentials: map<string, string>)
                 | RemoveStakeholder(name: string)

  ghost predicate Inv(m: Model) {
    true
  }

  function Init(): Model {
    map[]
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case AddStakeholder(name, credentials) => m[name := credentials]
    case RemoveStakeholder(name) => m - {name}
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

  lemma AddStakeholderEnsures(m: Model, name: string, credentials: map<string, string>)
    ensures Apply(m, AddStakeholder(name, credentials)) == m[name := credentials]
  {
  }

  lemma RemoveStakeholderEnsures(m: Model, name: string)
    ensures Apply(m, RemoveStakeholder(name)) == m - {name}
  {
  }
}

module F3_2_REQ_6Kernel refines Kernel {
  import D = F3_2_REQ_6Domain
}