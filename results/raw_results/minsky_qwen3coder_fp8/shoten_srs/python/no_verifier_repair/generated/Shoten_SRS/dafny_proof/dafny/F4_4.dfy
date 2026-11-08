include "Replay.dfy"

module F4_4Domain refines Domain {
  type Model = (string, map<string, int>)

  datatype Action = AddToCart(bookId: string) | ViewCart

  ghost predicate Inv(m: Model) {
    var (user, cart) := m;
    user != ""
  }

  function Init(): Model {
    ("", map[])
  }

  function Apply(m: Model, a: Action): Model {
    var (user, cart) := m;
    match a
    case AddToCart(bookId) =>
      if bookId in cart then
        (user, cart[bookId := cart[bookId] + 1])
      else
        (user, cart[bookId := 1])
    case ViewCart =>
      (user, cart)
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

  lemma AddToCartEnsures(m: Model, bookId: string)
    ensures var (user, cart) := Apply(m, AddToCart(bookId)); Inv((user, cart)) && bookId in cart && cart[bookId] == 1
  {
  }
}

module F4_4Kernel refines Kernel {
  import D = F4_4Domain
}