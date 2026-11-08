include "Replay.dfy"

module F4_3_2Domain refines Domain {
  type Model = (bool, map<string, PrintShop>)

  datatype Action = SearchButtonClicked | ResultsDisplayed

  datatype PrintShop = PrintShop(
    name: string,
    openTime: int,
    closeTime: int,
    rate: int
  )

  ghost predicate Inv(m: Model) {
    forall k | k in m.1 :: 
      0 <= m.1[k].openTime <= m.1[k].closeTime <= 24 &&
      m.1[k].rate >= 0
  }

  function Init(): Model {
    (false, map[])
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case SearchButtonClicked => 
      (true, m.1)
    case ResultsDisplayed => 
      (false, m.1)
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

  lemma SearchButtonClickedEnsuresSearching(m: Model)
    ensures Apply(m, SearchButtonClicked) == (true, m.1)
  {
  }

  lemma ResultsDisplayedEnsuresNotSearching(m: Model)
    ensures Apply(m, ResultsDisplayed) == (false, m.1)
  {
  }
}

module F4_3_2Kernel refines Kernel {
  import D = F4_3_2Domain
}