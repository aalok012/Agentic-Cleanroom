include "Replay.dfy"

module F4_13Domain refines Domain {
  type Model = map<string, seq<Order>>

  datatype Action = ViewPurchaseHistory

  ghost predicate Inv(m: Model) {
    forall user | user in m :: 
      forall order | order in m[user] ::
        order.date >= 0 && order.date <= 1000000 &&
        order.paymentMode != "" &&
        forall item | item in order.items ::
          item.title != "" && item.price >= 0 && item.quantity > 0
  }

  function Init(): Model {
    map[]
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case ViewPurchaseHistory => m
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

  datatype Order = Order(
    date: int,
    paymentMode: string,
    items: seq<Item>
  )

  datatype Item = Item(
    title: string,
    price: int,
    quantity: int
  )

  lemma ViewPurchaseHistoryDisplaysDateAndPaymentMode(m: Model)
    ensures forall user | user in m :: 
      forall order | order in m[user] ::
        order.date >= 0 && order.date <= 1000000 &&
        order.paymentMode != ""
  {
    assert forall user | user in m :: 
      forall order | order in m[user] ::
        order.date >= 0 && order.date <= 1000000 &&
        order.paymentMode != "";
  }

  lemma ViewPurchaseHistoryDisplaysBookDetails(m: Model)
    ensures forall user | user in m :: 
      forall order | order in m[user] ::
        forall item | item in order.items ::
          item.title != "" && item.price >= 0 && item.quantity > 0
  {
    assert forall user | user in m :: 
      forall order | order in m[user] ::
        forall item | item in order.items ::
          item.title != "" && item.price >= 0 && item.quantity > 0;
  }
}

module F4_13Kernel refines Kernel {
  import D = F4_13Domain
}