include "Replay.dfy"

module F4_4Domain refines Domain {
  type Model = map<string, int>

  datatype Action = AddToCart(bookId: string, price: int)

  ghost predicate Inv(m: Model) {
    forall k | k in m :: m[k] > 0
  }

  function Init(): Model {
    map[]
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case AddToCart(bookId, price) => m[bookId := price]
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

  lemma AddToCartPreservesTotal(m: Model, a: Action)
    ensures Inv(m) ==> Inv(Normalize(Apply(m, a)))
  {
  }
}

module F4_4Kernel refines Kernel {
  import D = F4_4Domain
}