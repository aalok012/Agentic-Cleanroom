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
    let (_, shops) = m;
    forall k | k in shops :: 
      0 <= shops[k].openTime <= shops[k].closeTime <= 24 &&
      shops[k].rate >= 0
  }

  function Init(): Model {
    (false, map[])
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case SearchButtonClicked => 
      let (_, shops) = m;
      (true, shops)
    case ResultsDisplayed => 
      let (searching, shops) = m;
      (false, shops)
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
    ensures Apply(m, SearchButtonClicked) == (true, (let (_, shops) = m; shops))
  {
  }

  lemma ResultsDisplayedEnsuresNotSearching(m: Model)
    ensures Apply(m, ResultsDisplayed) == (false, (let (_, shops) = m; shops))
  {
  }
}

module F4_3_2Kernel refines Kernel {
  import D = F4_3_2Domain
}