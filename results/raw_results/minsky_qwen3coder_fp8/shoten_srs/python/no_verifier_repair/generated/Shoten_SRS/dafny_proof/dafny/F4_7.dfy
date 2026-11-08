include "Replay.dfy"

module F4_7Domain refines Domain {
  datatype Action = ViewTotal | Purchase | EnterDeliveryInfo | CompleteCheckout | CompleteTransaction

  type Model = (map<string, int>, map<string, (string, int)>, map<string, (string, int)>, string, string)

  predicate Inv(m: Model) {
    var (cart, purchased, deliveryInfo, paymentInfo, userInfo) := m;
    forall k | k in cart && k in purchased :: cart[k] == 0
  }

  function Init(): Model {
    (map[], map[], map[], "", "")
  }

  function Apply(m: Model, a: Action): Model {
    var (cart, purchased, deliveryInfo, paymentInfo, userInfo) := m;
    match a
    case ViewTotal =>
      var totalCost := 0;
      var cartCopy := cart;
      while cartCopy != map[]
        invariant cartCopy == cart
        invariant totalCost == sum(k | k in cart && cart[k] != 0 :: cart[k] * purchased[k].2)
      {
        var k := cartCopy.keys.min();
        if k in cartCopy && cartCopy[k] != 0 {
          totalCost := totalCost + cartCopy[k] * purchased[k].2;
          cartCopy := cartCopy - {k};
        } else {
          cartCopy := cartCopy - {k};
        }
      }
      m
    case Purchase =>
      var newPurchased := purchased;
      var newCart := cart;
      var keys := cart.keys;
      foreach k in keys {
        if k in cart && cart[k] != 0 {
          newPurchased := newPurchased + [k := (purchased[k].1, cart[k])];
          newCart := newCart - {k};
        }
      }
      (newCart, newPurchased, deliveryInfo, paymentInfo, userInfo)
    case EnterDeliveryInfo =>
      var newDeliveryInfo := deliveryInfo + [userInfo := ("", 0)];
      (cart, purchased, newDeliveryInfo, paymentInfo, userInfo)
    case CompleteCheckout =>
      (cart, purchased, deliveryInfo, "payment info", userInfo)
    case CompleteTransaction =>
      (map[], map[], deliveryInfo, paymentInfo, userInfo)
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

  lemma ViewTotalCorrect(m: Model)
    ensures Apply(m, ViewTotal) == m
  {
  }

  lemma PurchaseRemovesItems(m: Model)
    ensures forall k | k in (Apply(m, Purchase)).0 :: (Apply(m, Purchase)).0[k] == 0
  {
  }

  lemma CompleteTransactionClearsCart(m: Model)
    ensures (Apply(m, CompleteTransaction)).0 == map[]
  {
  }
}

module F4_7Kernel refines Kernel {
  import D = F4_7Domain
}