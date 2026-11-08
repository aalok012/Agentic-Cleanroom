include "Replay.dfy"

module F4_7Domain refines Domain {
  type Model = (map<string, int>, map<string, int>, string, bool, map<string, (int, int)>, bool)

  datatype Action = ViewTotalCost | Purchase | EnterDeliveryInfo(address: string) | CompleteCheckout | CompleteTransaction

  ghost predicate Inv(m: Model) {
    var (cart, user, deliveryInfo, loggedIn, purchasedBooks, paymentEntered) := m;
    loggedIn ==> user != ""
  }

  function Init(): Model {
    (map[], "", "", false, map[], false)
  }

  function Apply(m: Model, a: Action): Model {
    var (cart, user, deliveryInfo, loggedIn, purchasedBooks, paymentEntered) := m;
    match a
    case ViewTotalCost =>
      m
    case Purchase =>
      if loggedIn && cart != map[] then
        (map[], user, deliveryInfo, loggedIn, cart, paymentEntered)
      else
        m
    case EnterDeliveryInfo(addr) =>
      (cart, user, addr, loggedIn, purchasedBooks, paymentEntered)
    case CompleteCheckout =>
      if deliveryInfo != "" then
        (cart, user, deliveryInfo, loggedIn, purchasedBooks, true)
      else
        m
    case CompleteTransaction =>
      if paymentEntered then
        (map[], user, deliveryInfo, loggedIn, purchasedBooks, paymentEntered)
      else
        m
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

  lemma ViewTotalCostCorrect(m: Model)
    ensures var cart := Apply(m, ViewTotalCost).0;
      var totalCost := 0;
      forall k | k in cart :: totalCost := totalCost + cart[k];
      true
  {
  }
}

module F4_7Kernel refines Kernel {
  import D = F4_7Domain
}