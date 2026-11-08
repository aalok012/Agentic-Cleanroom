include "Replay.dfy"

module F4_5Domain refines Domain {
  type Model = map<string, int>

  datatype Action = Remove(book: string)

  ghost predicate Inv(m: Model) {
    forall k | k in m :: m[k] > 0
  }

  function Init(): Model {
    map[]
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case Remove(book) => if book in m then m - {book} else m
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

  lemma RemoveEnsuresNonEmpty(m: Model, book: string)
    requires Inv(m)
    requires book in m
    ensures !(book in Apply(m, Remove(book)))
    ensures forall k | k in Apply(m, Remove(book)) :: Apply(m, Remove(book))[k] > 0
  {
  }
}

module F4_5Kernel refines Kernel {
  import D = F4_5Domain
}