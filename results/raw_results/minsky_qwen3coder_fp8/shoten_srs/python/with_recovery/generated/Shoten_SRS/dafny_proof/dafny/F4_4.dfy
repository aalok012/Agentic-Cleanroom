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
    match a
    case AddToCart(bookId) =>
      var (user, cart) := m;
      if bookId in cart then
        (user, cart[bookId := cart[bookId] + 1])
      else
        (user, cart[bookId := 1])
    case ViewCart =>
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

  lemma AddToCartEnsures(m: Model, bookId: string)
    ensures match Apply(m, AddToCart(bookId))
    case (_, cart) => bookId in cart && cart[bookId] > 0
  {
  }

  lemma ViewCartEnsures(m: Model)
    ensures match Apply(m, ViewCart)
    case (_, cart) => 
      var total := 0;
      forall k | k in cart :: total += cart[k]
  {
  }
}

module F4_4Kernel refines Kernel {
  import D = F4_4Domain
}