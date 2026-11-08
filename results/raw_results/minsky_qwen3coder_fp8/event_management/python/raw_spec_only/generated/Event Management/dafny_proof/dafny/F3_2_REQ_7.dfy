include "Replay.dfy"

module F3_2_REQ_7Domain refines Domain {
  type Model = map<string, string>

  datatype Action = 
    Add(key: string, value: string) |
    Update(key: string, value: string) |
    Delete(key: string) |
    Retrieve(key: string)

  ghost predicate Inv(m: Model) {
    true
  }

  function Init(): Model {
    map[]
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case Add(k, v) => m[k := v]
    case Update(k, v) => if k in m then m[k := v] else m
    case Delete(k) => if k in m then m - {k} else m
    case Retrieve(k) => m
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

  lemma AddEnsures(m: Model, k: string, v: string)
    ensures Apply(m, Add(k, v)) == m[k := v]
  {
  }

  lemma UpdateEnsures(m: Model, k: string, v: string)
    ensures Apply(m, Update(k, v)) == (if k in m then m[k := v] else m)
  {
  }

  lemma DeleteEnsures(m: Model, k: string)
    ensures Apply(m, Delete(k)) == (if k in m then m - {k} else m)
  {
  }

  lemma RetrieveEnsures(m: Model, k: string)
    ensures Apply(m, Retrieve(k)) == m
  {
  }
}

module F3_2_REQ_7Kernel refines Kernel {
  import D = F3_2_REQ_7Domain
}