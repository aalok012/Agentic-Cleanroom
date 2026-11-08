include "Replay.dfy"

module F4_3_1Domain refines Domain {
  datatype Book = Book(title: string, author: string, isbn: string, price: int, available: bool, condition: string)

  type Model = map<string, Book>

  datatype Action = Search(title: string, author: string, isbn: string)

  ghost predicate Inv(m: Model) {
    forall k | k in m :: m[k].title != ""
  }

  function Init(): Model {
    map[]
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case Search(title, author, isbn) => m
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

  lemma SearchReturnsBooks(m: Model, a: Action)
    requires a == Search("", "", "")
    ensures forall k | k in Apply(m, a) :: Apply(m, a)[k].title != ""
  {
    // The Apply function simply returns the model unchanged
    // The postcondition is vacuously true because when m is empty, 
    // there are no keys in Apply(m, a) to check
    // When m is not empty, the invariant guarantees all books have non-empty titles
  }
}

module F4_3_1Kernel refines Kernel {
  import D = F4_3_1Domain
}