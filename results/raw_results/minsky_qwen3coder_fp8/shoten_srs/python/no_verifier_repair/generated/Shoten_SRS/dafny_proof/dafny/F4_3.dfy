include "Replay.dfy"

module F4_3Domain refines Domain {
  type Model = map<string, set<string>>

  datatype Action = Search(query: string)

  ghost predicate Inv(m: Model) {
    true
  }

  function Init(): Model {
    map[]
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case Search(query) => 
      map k | k in m :: 
        if k == query then m[k] else 
          if query in m[k] then m[k] - {query} else m[k]
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

  lemma SearchResultMatchesQuery(m: Model, query: string)
    ensures (forall k | k in Apply(m, Search(query)) :: 
      (k == query ==> Apply(m, Search(query))[k] == m[k]) &&
      (k != query ==> Apply(m, Search(query))[k] == m[k]))
  {
  }
}

module F4_3Kernel refines Kernel {
  import D = F4_3Domain
}