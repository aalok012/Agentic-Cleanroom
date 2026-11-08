include "Replay.dfy"

module F4_9Domain refines Domain {
  datatype Book = Book(
    name: string,
    quantity: int,
    lendable: bool,
    sellable: bool,
    isbn: string,
    author: string,
    rentalPrice: int,
    sellingPrice: int
  )

  datatype Action = AddBook(book: Book)

  type Model = map<string, Book>

  ghost predicate Inv(m: Model) {
    forall k | k in m :: 
      m[k].quantity >= 0 &&
      m[k].rentalPrice >= 0 &&
      m[k].sellingPrice >= 0 &&
      m[k].isbn != ""
  }

  function Init(): Model {
    map[]
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case AddBook(book) => m[book.isbn := book]
  }

  function Normalize(m: Model): Model {
    m
  }

  lemma InitSatisfiesInv()
    ensures Inv(Init())
  {
    assert forall k | k in Init() :: 
      Init()[k].quantity >= 0 &&
      Init()[k].rentalPrice >= 0 &&
      Init()[k].sellingPrice >= 0 &&
      Init()[k].isbn != "";
  }

  lemma StepPreservesInv(m: Model, a: Action)
    ensures Inv(Normalize(Apply(m, a)))
  {
    assert forall k | k in Apply(m, a) :: 
      Apply(m, a)[k].quantity >= 0 &&
      Apply(m, a)[k].rentalPrice >= 0 &&
      Apply(m, a)[k].sellingPrice >= 0 &&
      Apply(m, a)[k].isbn != "";
  }

  lemma AddBookEnsuresInv(m: Model, book: Book)
    ensures Inv(m[book.isbn := book])
  {
    assert forall k | k in m[book.isbn := book] :: 
      (k == book.isbn ==> 
        m[book.isbn := book][k].quantity >= 0 &&
        m[book.isbn := book][k].rentalPrice >= 0 &&
        m[book.isbn := book][k].sellingPrice >= 0 &&
        m[book.isbn := book][k].isbn != "") &&
      (k != book.isbn ==> 
        m[book.isbn := book][k].quantity >= 0 &&
        m[book.isbn := book][k].rentalPrice >= 0 &&
        m[book.isbn := book][k].sellingPrice >= 0 &&
        m[book.isbn := book][k].isbn != "");
  }
}

module F4_9Kernel refines Kernel {
  import D = F4_9Domain
}