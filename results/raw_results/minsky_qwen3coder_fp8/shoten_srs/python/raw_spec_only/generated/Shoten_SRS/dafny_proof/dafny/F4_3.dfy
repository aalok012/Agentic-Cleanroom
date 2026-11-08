include "Replay.dfy"

module F4_3Domain refines Domain {
  type Model = map<string, set<string>>

  datatype Action = Search(query: string)

  ghost predicate Inv(m: Model) {
    forall k | k in m :: k != ""
  }

  function Init(): Model {
    map[]
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case Search(q) =>
      if q == "" then m
      else map k | k in m && k.Contains(q) :: m[k]
  }

  function Normalize(m: Model): Model {
    map k | k in m && k != "" :: m[k]
  }

  lemma InitSatisfiesInv()
    ensures Inv(Init())
  {
  }

  lemma StepPreservesInv(m: Model, a: Action)
    ensures Inv(Normalize(Apply(m, a)))
  {
  }

  lemma SearchEmptyQueryDoesNotChangeModel(m: Model, a: Action)
    requires a == Search("")
    ensures Apply(m, a) == m
  {
  }
}

module F4_3Kernel refines Kernel {
  import D = F4_3Domain
}