include "Replay.dfy"

module F4_13Domain refines Domain {
  type Model = (map<int, Purchase>, map<int, Order>)

  datatype Action = ViewPurchaseHistory | ViewOrderDetails(orderId: int)

  ghost predicate Inv(m: Model) {
    let (purchases, orders) = m; true
  }

  function Init(): Model {
    (map[], map[])
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case ViewPurchaseHistory => m
    case ViewOrderDetails(orderId) => m
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

  lemma ViewPurchaseHistoryEnsures(m: Model)
    ensures let (purchases, orders) = m; 
            |purchases| == 0 ==> purchases == map[]
  {
  }
}

module F4_13Kernel refines Kernel {
  import D = F4_13Domain
}