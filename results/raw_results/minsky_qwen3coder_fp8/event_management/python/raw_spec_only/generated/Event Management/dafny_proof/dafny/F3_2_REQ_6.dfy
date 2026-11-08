include "Replay.dfy"

module F3_2_REQ_6Domain refines Domain {
  type Model = map<string, map<string, string>>

  datatype Action = AddStakeholder(name: string, credentials: map<string, string>)
                 | RemoveStakeholder(name: string)
                 | UpdateStakeholder(name: string, field: string, value: string)

  ghost predicate Inv(m: Model) {
    forall name | name in m :: 
      forall field | field in m[name] :: 
        m[name][field] != ""
  }

  function Init(): Model {
    map[]
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case AddStakeholder(name, credentials) => m[name := credentials]
    case RemoveStakeholder(name) => m - {name}
    case UpdateStakeholder(name, field, value) =>
      if name in m then
        m[name][field := value]
      else
        m
  }

  function Normalize(m: Model): Model {
    map name | name in m && forall field | field in m[name] :: m[name][field] != "" :: m[name]
  }

  lemma InitSatisfiesInv()
    ensures Inv(Init())
  {
  }

  lemma StepPreservesInv(m: Model, a: Action)
    ensures Inv(Normalize(Apply(m, a)))
  {
  }

  lemma AddStakeholderPreservesInv(m: Model, name: string, credentials: map<string, string>)
    ensures Inv(Normalize(Apply(m, AddStakeholder(name, credentials))))
  {
  }

  lemma RemoveStakeholderPreservesInv(m: Model, name: string)
    ensures Inv(Normalize(Apply(m, RemoveStakeholder(name))))
  {
  }

  lemma UpdateStakeholderPreservesInv(m: Model, name: string, field: string, value: string)
    ensures Inv(Normalize(Apply(m, UpdateStakeholder(name, field, value))))
  {
  }
}

module F3_2_REQ_6Kernel refines Kernel {
  import D = F3_2_REQ_6Domain
}