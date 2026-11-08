include "Replay.dfy"

module F4_5Domain refines Domain {
  type Model = map<string, int>

  datatype Action = RemoveBook(bookId: string)

  ghost predicate Inv(m: Model) {
    forall k | k in m :: m[k] > 0
  }

  function Init(): Model {
    map[]
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case RemoveBook(bookId) => m - {bookId}
    }
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

  lemma RemoveBookEnsures(m: Model, bookId: string)
    requires Inv(m)
    requires bookId in m
    ensures bookId !in Apply(m, RemoveBook(bookId))
  {
  }
}

module F4_5Kernel refines Kernel {
  import D = F4_5Domain
}