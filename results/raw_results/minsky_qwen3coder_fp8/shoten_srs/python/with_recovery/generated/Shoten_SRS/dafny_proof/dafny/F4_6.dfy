include "Replay.dfy"

module F4_6Domain refines Domain {
  datatype Action =
    | InitiateRent
    | EnterRentalPeriod(period: int)
    | ConfirmRentalPeriod
    | EnterDeliveryInfo(address: string, contact: string)
    | EnterPaymentInfo(payment: string)
    | CompleteTransaction

  type Model = (bool, map<string, int>, map<string, int>, int, string, string, string, map<string, (int, int)>, bool)

  ghost predicate Inv(m: Model) {
    var (loggedIn, cart, rented, period, address, contact, payment, prices, completed) := m;
    loggedIn && 
    (cart == map[]) == (rented == map[]) &&
    (period >= 0) &&
    (address != "") == (contact != "") &&
    (payment != "") == (completed)
  }

  function Init(): Model {
    (true, map[], map[], 0, "", "", "", map[], false)
  }

  function Apply(m: Model, a: Action): Model {
    var (loggedIn, cart, rented, period, address, contact, payment, prices, completed) := m;
    match a
    case InitiateRent =>
      if cart == map[] then m else (loggedIn, cart, map[], 0, address, contact, payment, prices, completed)
    case EnterRentalPeriod(p) =>
      (loggedIn, cart, rented, p, address, contact, payment, prices, completed)
    case ConfirmRentalPeriod =>
      if period <= 0 then m else (loggedIn, cart, rented, period, address, contact, payment, 
        map k | k in cart :: (cart[k], period), completed)
    case EnterDeliveryInfo(addr, cont) =>
      (loggedIn, cart, rented, period, addr, cont, payment, prices, completed)
    case EnterPaymentInfo(pay) =>
      (loggedIn, cart, rented, period, address, contact, pay, prices, completed)
    case CompleteTransaction =>
      if payment == "" || address == "" || contact == "" || period <= 0 then m else 
        (loggedIn, map[], map[], 0, "", "", "", map[], true)
  }

  function Normalize(m: Model): Model {
    var (loggedIn, cart, rented, period, address, contact, payment, prices, completed) := m;
    if period < 0 then (loggedIn, cart, rented, 0, address, contact, payment, prices, completed)
    else if period > 1000 then (loggedIn, cart, rented, 1000, address, contact, payment, prices, completed)
    else m
  }

  lemma InitSatisfiesInv()
    ensures Inv(Init())
  {
  }

  lemma StepPreservesInv(m: Model, a: Action)
    ensures Inv(Normalize(Apply(m, a)))
  {
    assert Inv(m) ==> Inv(Apply(m, a));
    assert Inv(Apply(m, a)) ==> Inv(Normalize(Apply(m, a)));
  }

  lemma RentInitiated(m: Model)
    requires Inv(m)
    ensures (match Apply(m, InitiateRent) {
      case (_, newCart, newRented, _, _, _, _, _, _) => 
        newCart == map[] || newRented == map[]
    })
  {
    assert Inv(m);
    var (loggedIn, cart, rented, period, address, contact, payment, prices, completed) := m;
    var result := Apply(m, InitiateRent);
    var (_, newCart, newRented, _, _, _, _, _, _) := result;
    if cart == map[] {
      assert newCart == map[];
      assert newRented == map[];
    } else {
      assert newCart == cart;
      assert newRented == map[];
    }
  }
}

module F4_6Kernel refines Kernel {
  import D = F4_6Domain
}