include "Replay.dfy"

module F4_3_2Domain refines Domain {
  type Model = (bool, map<string, (int, int, int)>)

  datatype Action = SearchButtonClicked | ResultsDisplayed

  ghost predicate Inv(m: Model) {
    var (searching, shops) := m;
    searching ==> shops == map[]
  }

  function Init(): Model {
    (false, map[])
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case SearchButtonClicked =>
      var (searching, shops) := m;
      if searching then m else (true, map[])
    case ResultsDisplayed =>
      var (searching, shops) := m;
      if searching then
        (false, map[
          "ShopA" := (9, 17, 50),
          "ShopB" := (8, 18, 60),
          "ShopC" := (10, 16, 45)
        ])
      else m
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
    ensures Apply(m, SearchButtonClicked) == (true, map[])
  {
  }

  lemma ResultsDisplayedEnsuresAccurateInfo(m: Model)
    ensures Apply(m, ResultsDisplayed) == (false, map[
      "ShopA" := (9, 17, 50),
      "ShopB" := (8, 18, 60),
      "ShopC" := (10, 16, 45)
    ])
  {
  }
}

module F4_3_2Kernel refines Kernel {
  import D = F4_3_2Domain
}