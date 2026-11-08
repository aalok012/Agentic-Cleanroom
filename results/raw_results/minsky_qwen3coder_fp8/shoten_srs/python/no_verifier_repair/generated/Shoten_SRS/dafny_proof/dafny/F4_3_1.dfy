include "Replay.dfy"

module F4_3_1Domain refines Domain {
  type Model = (bool, map<string, Book>)

  datatype Action = SearchBook

  ghost predicate Inv(m: Model) {
    var (_, books) := m;
    true
  }

  function Init(): Model {
    (false, map[])
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case SearchBook => 
      var (_, books) := m;
      (true, books)
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

  lemma SearchBookDisplaysInterface(m: Model)
    requires m == Init()
    ensures var (searching, _) := Apply(m, SearchBook);
            searching == true
  {
  }
}

module F4_3_1Kernel refines Kernel {
  import D = F4_3_1Domain
}

datatype Book = Book(
  title: string,
  author: string,
  isbn: string,
  price: int,
  availability: bool,
  condition: string,
  coverImage: string
)