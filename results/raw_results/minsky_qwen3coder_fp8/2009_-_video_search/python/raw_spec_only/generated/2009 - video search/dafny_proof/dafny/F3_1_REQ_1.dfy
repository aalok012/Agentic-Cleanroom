include "Replay.dfy"

module F3_1_REQ_1Domain refines Domain {
  type Model = map<string, string>

  datatype Action = Search(query: string)

  ghost predicate Inv(m: Model) {
    true
  }

  function Init(): Model {
    map[]
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case Search(query) => m
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

  lemma SearchDoesNotChangeModel(m: Model, a: Action)
    requires a == Search("")
    ensures Apply(m, a) == m
  {
  }
}

module F3_1_REQ_1Kernel refines Kernel {
  import D = F3_1_REQ_1Domain
}