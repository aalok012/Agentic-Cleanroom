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
      map k | k in m && exists w | w in query.Split(' ') && w != "" && w in m[k] :: m[k]
    }
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

  lemma SearchResultMatchesQuery(m: Model, a: Action)
    requires a == Search(_)
    ensures forall k | k in Apply(m, a) :: 
      exists q | q in m && q == k :: 
        exists w | w in q && w in a.query.Split(' ') && w != "" :: true
  {
  }
}

module F4_3Kernel refines Kernel {
  import D = F4_3Domain
}