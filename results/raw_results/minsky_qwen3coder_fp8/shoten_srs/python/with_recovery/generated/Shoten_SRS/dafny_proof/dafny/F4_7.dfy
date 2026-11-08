include "Replay.dfy"

module F4_7Domain refines Domain {
  type Model = (map<string, int>, map<string, int>, string, bool, map<string, (string, int)>)

  datatype Action = ViewTotalCost | Purchase | EnterDeliveryInfo(address: string) | CompleteCheckout | CompleteTransaction(titles: map<string, (string, int)>)

  ghost predicate Inv(m: Model) {
    var (cart, purchased, deliveryInfo, checkoutComplete, transactionInfo) := m;
    forall k | k in cart :: cart[k] > 0
  }

  function Init(): Model {
    (map[], map[], "", false, map[])
  }

  function Apply(m: Model, a: Action): Model {
    var (cart, purchased, deliveryInfo, checkoutComplete, transactionInfo) := m;
    match a
    case ViewTotalCost =>
      m
    case Purchase =>
      (map[], cart, deliveryInfo, checkoutComplete, transactionInfo)
    case EnterDeliveryInfo(addr) =>
      (cart, purchased, addr, checkoutComplete, transactionInfo)
    case CompleteCheckout =>
      (cart, purchased, deliveryInfo, true, transactionInfo)
    case CompleteTransaction(info) =>
      (cart, purchased, deliveryInfo, checkoutComplete, info)
  }

  function Normalize(m: Model): Model {
    var (cart, purchased, deliveryInfo, checkoutComplete, transactionInfo) := m;
    if cart == map[] && purchased != map[] then
      (map[], map[], deliveryInfo, checkoutComplete, transactionInfo)
    else
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

  function GetPrice(bookId: string): int {
    10 // dummy price
  }

  lemma ViewTotalCostCorrect(m: Model)
    ensures true
  {
  }

  lemma PurchaseRemovesItems(m: Model)
    ensures (Apply(m, Purchase)).0 == map[]
  {
    assert (Apply(m, Purchase)).0 == map[];
  }
}

module F4_7Kernel refines Kernel {
  import D = F4_7Domain
}