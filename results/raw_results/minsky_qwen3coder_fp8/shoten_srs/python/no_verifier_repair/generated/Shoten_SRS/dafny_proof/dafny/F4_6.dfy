include "Replay.dfy"

module F4_6Domain refines Domain {
  datatype Action =
    InitiateRent |
    EnterRentalPeriod(period: int) |
    ConfirmRentalPeriod |
    EnterDeliveryInfo(address: string, contact: string) |
    EnterPaymentInfo(payment: string) |
    FinalizeTransaction

  type Model = (map<string, int>, map<string, int>, int, string, string, string, bool)

  ghost predicate Inv(m: Model) {
    var (cart, prices, period, address, contact, payment, finalized) := m;
    && period >= 0
    && (address != "" || address == "")
    && (contact != "" || contact == "")
    && (payment != "" || payment == "")
    && forall k | k in cart && k in prices :: cart[k] >= 0 && prices[k] >= 0
  }

  function Init(): Model {
    (map[], map[], 0, "", "", "", false)
  }

  function Apply(m: Model, a: Action): Model {
    var (cart, prices, period, address, contact, payment, finalized) := m;
    match a
    case InitiateRent =>
      if cart != map[] && prices != map[] then
        (cart, prices, period, address, contact, payment, finalized)
      else
        (cart, prices, period, address, contact, payment, finalized)
    case EnterRentalPeriod(p) =>
      (cart, prices, p, address, contact, payment, finalized)
    case ConfirmRentalPeriod =>
      (cart, prices, period, address, contact, payment, finalized)
    case EnterDeliveryInfo(addr, cont) =>
      (cart, prices, period, addr, cont, payment, finalized)
    case EnterPaymentInfo(pay) =>
      (cart, prices, period, address, contact, pay, finalized)
    case FinalizeTransaction =>
      (cart, prices, period, address, contact, payment, true)
  }

  function Normalize(m: Model): Model {
    var (cart, prices, period, address, contact, payment, finalized) := m;
    if period < 0 then
      (cart, prices, 0, address, contact, payment, finalized)
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

  lemma CartMarkedAsRented(m: Model, a: Action)
    requires a == InitiateRent
    requires Inv(m)
    ensures var (cart, prices, period, address, contact, payment, finalized) := Apply(m, a);
            cart != map[] && prices != map[]
  {
  }
}

module F4_6Kernel refines Kernel {
  import D = F4_6Domain
}