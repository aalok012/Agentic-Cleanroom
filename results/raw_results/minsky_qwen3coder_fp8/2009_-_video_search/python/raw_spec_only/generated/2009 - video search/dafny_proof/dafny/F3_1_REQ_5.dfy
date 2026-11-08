include "Replay.dfy"

module F3_1_REQ_5Domain refines Domain {
  type Model = (string, map<string, string>)

  datatype Action = Search(query: string)

  ghost predicate Inv(m: Model) {
    var (_, results) := m;
    true
  }

  function Init(): Model {
    ("", map[])
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case Search(query) =>
      if query == "" then
        ("No results were found for this search.", map[])
      else
        (query, map[])
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

  lemma SearchEmptyQueryEnsuresNoResultsMessage(m: Model)
    ensures Apply(m, Search("")) == ("No results were found for this search.", map[])
  {
  }
}

module F3_1_REQ_5Kernel refines Kernel {
  import D = F3_1_REQ_5Domain
}