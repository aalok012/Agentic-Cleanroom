include "Replay.dfy"

module F3_1_REQ_5Domain refines Domain {
  type Model = string

  datatype Action = SearchNoResults

  ghost predicate Inv(m: Model) {
    m == "No results were found for this search." || m == ""
  }

  function Init(): Model {
    ""
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case SearchNoResults => "No results were found for this search."
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

  lemma SearchNoResultsShowsMessage(m: Model)
    requires Inv(m)
    ensures Apply(m, SearchNoResults) == "No results were found for this search."
  {
  }
}

module F3_1_REQ_5Kernel refines Kernel {
  import D = F3_1_REQ_5Domain
}