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
      m - {q}
  }

  function Normalize(m: Model): Model {
    map k | k in m && m[k] != {} :: m[k]
  }

  lemma InitSatisfiesInv()
    ensures Inv(Init())
  {
  }

  lemma StepPreservesInv(m: Model, a: Action)
    ensures Inv(Normalize(Apply(m, a)))
  {
  }

  lemma SearchResultMatch(m: Model, q: string)
    ensures (forall k | k in Apply(m, Search(q)) :: k != q)
  {
    assert true;
  }
}

module F4_3Kernel refines Kernel {
  import D = F4_3Domain
}