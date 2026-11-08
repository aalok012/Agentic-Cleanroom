include "Replay.dfy"

module F4_13Domain refines Domain {
  datatype Purchase = Purchase(date: int, paymentMode: string)
  datatype Order = Order(items: map<string, (int, int)>) // title -> (price, quantity)

  type Model = (map<int, Purchase>, map<int, Order>)

  datatype Action = ViewPurchaseHistory | ViewOrderDetails(orderId: int)

  ghost predicate Inv(m: Model) {
    true
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
    ensures |m.0| == 0 ==> m.0 == map[]
  {
  }
}

module F4_13Kernel refines Kernel {
  import D = F4_13Domain
}