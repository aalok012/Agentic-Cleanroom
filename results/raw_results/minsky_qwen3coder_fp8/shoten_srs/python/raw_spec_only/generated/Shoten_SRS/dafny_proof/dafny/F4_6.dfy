include "Replay.dfy"

module F4_6Domain refines Domain {
  type Model = (map<string, int>, map<string, int>, map<string, int>, string, string, string, string)

  datatype Action =
    | RentBooks
    | EnterRentalPeriod(period: string)
    | DisplayRentCharges
    | EnterDeliveryInfo(deliveryInfo: string)
    | EnterPaymentInfo(paymentInfo: string)
    | ConfirmTransaction

  ghost predicate Inv(m: Model) {
    var (cart, rentCharges, bookPrices, period, deliveryInfo, paymentInfo, transactionStatus) := m;
    true
  }

  function Init(): Model {
    (map[], map[], map[], "", "", "", "")
  }

  function Apply(m: Model, a: Action): Model {
    var (cart, rentCharges, bookPrices, period, deliveryInfo, paymentInfo, transactionStatus) := m;
    match a
    case RentBooks =>
      (cart, rentCharges, bookPrices, period, deliveryInfo, paymentInfo, "renting")
    case EnterRentalPeriod(p) =>
      (cart, rentCharges, bookPrices, p, deliveryInfo, paymentInfo, transactionStatus)
    case DisplayRentCharges =>
      (cart, rentCharges, bookPrices, period, deliveryInfo, paymentInfo, transactionStatus)
    case EnterDeliveryInfo(d) =>
      (cart, rentCharges, bookPrices, period, d, paymentInfo, transactionStatus)
    case EnterPaymentInfo(p) =>
      (cart, rentCharges, bookPrices, period, deliveryInfo, p, transactionStatus)
    case ConfirmTransaction =>
      (map[], map[], map[], "", "", "", "completed")
  }

  function Normalize(m: Model): Model {
    var (cart, rentCharges, bookPrices, period, deliveryInfo, paymentInfo, transactionStatus) := m;
    if cart == map[] && period == "" && deliveryInfo == "" && paymentInfo == "" && transactionStatus == "completed"
    then (map[], map[], map[], "", "", "", "")
    else m
  }

  lemma InitSatisfiesInv()
    ensures Inv(Init())
  {
  }

  lemma StepPreservesInv(m: Model, a: Action)
    ensures Inv(Normalize(Apply(m, a)))
  {
  }

  lemma RentBooksEnsures(m: Model)
    ensures match Apply(m, RentBooks)
      case (cart, rentCharges, bookPrices, period, deliveryInfo, paymentInfo, transactionStatus) =>
        transactionStatus == "renting"
    ensures Inv(Normalize(Apply(m, RentBooks)))
  {
  }
}

module F4_6Kernel refines Kernel {
  import D = F4_6Domain
}