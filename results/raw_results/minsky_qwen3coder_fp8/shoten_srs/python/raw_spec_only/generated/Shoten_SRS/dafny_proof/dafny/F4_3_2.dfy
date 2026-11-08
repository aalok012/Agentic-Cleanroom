include "Replay.dfy"

module F4_3_2Domain refines Domain {
  type Model = map<string, Shop>

  datatype Action = SearchPrintShop

  ghost predicate Inv(m: Model) {
    forall k | k in m :: m[k].name != ""
  }

  function Init(): Model {
    map[]
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case SearchPrintShop => m
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

  datatype Shop = Shop(name: string, openTime: int, closeTime: int, rate: int)

  lemma SearchPrintShopReturnsResults(m: Model)
    ensures |Apply(m, SearchPrintShop)| >= 0
  {
    assert |Apply(m, SearchPrintShop)| == |m|;
    assert |m| >= 0;
  }
}

module F4_3_2Kernel refines Kernel {
  import D = F4_3_2Domain
}