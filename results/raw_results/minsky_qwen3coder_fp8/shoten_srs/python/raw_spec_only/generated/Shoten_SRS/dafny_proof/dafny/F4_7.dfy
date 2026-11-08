include "Replay.dfy"

module F4_7Domain refines Domain {
  datatype Action = 
    PurchaseBooks | 
    DisplayCartTotal | 
    EnterDeliveryInfo | 
    PromptPaymentInfo | 
    DisplayTransactionDetails

  type Model = (map<string, int>, map<string, string>, string, string, map<string, (string, int, int)>)

  ghost predicate Inv(m: Model) {
    var (cart, user, delivery, payment, transaction) := m;
    && (forall k | k in cart :: cart[k] > 0)
    && (forall k | k in user :: user[k] != "")
    && (delivery != "")
    && (payment != "")
    && (forall k | k in transaction :: transaction[k].0 != "" && transaction[k].2 > 0)
  }

  function Init(): Model {
    (map[], map[], "", "", map[])
  }

  function Apply(m: Model, a: Action): Model {
    var (cart, user, delivery, payment, transaction) := m;
    match a
    case PurchaseBooks =>
      var newTransaction := map k | k in cart :: (user[k], cart[k], cart[k]);
      (map[], user, delivery, payment, newTransaction)
    case DisplayCartTotal =>
      (cart, user, delivery, payment, transaction)
    case EnterDeliveryInfo =>
      (cart, user, "123 Main St", payment, transaction)
    case PromptPaymentInfo =>
      (cart, user, delivery, "Visa ending in 1234", transaction)
    case DisplayTransactionDetails =>
      (cart, user, delivery, payment, transaction)
  }

  function Normalize(m: Model): Model {
    var (cart, user, delivery, payment, transaction) := m;
    if delivery == "" then
      (cart, user, "123 Main St", payment, transaction)
    else if payment == "" then
      (cart, user, delivery, "Visa ending in 1234", transaction)
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

  lemma PurchaseBooksEnsures(m: Model)
    ensures (match Apply(m, PurchaseBooks) {
      case (_, _, _, _, t) => 
        forall k | k in t :: t[k].0 != "" && t[k].2 > 0
    })
  {
    var result := Apply(m, PurchaseBooks);
    assert forall k | k in result.4 :: result.4[k].0 != "" && result.4[k].2 > 0;
  }
}

module F4_7Kernel refines Kernel {
  import D = F4_7Domain
}