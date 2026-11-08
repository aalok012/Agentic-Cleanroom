include "Replay.dfy"

module F4_5Domain refines Domain {
  type Model = (string, map<string, int>)

  datatype Action = RemoveBook(bookId: string)

  ghost predicate Inv(m: Model) {
    var (user, cart) := m;
    user != "" && cart != map[]
  }

  function Init(): Model {
    ("user123", map[])
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case RemoveBook(bookId) =>
      var (user, cart) := m;
      if bookId in cart then
        (user, cart - {bookId})
      else
        m
  }

  function Normalize(m: Model): Model {
    var (user, cart) := m;
    if user == "" || cart == map[] then
      Init()
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

  lemma RemoveBookEnsures(m: Model, bookId: string)
    ensures match Apply(m, RemoveBook(bookId))
      case (user, cart) =>
        var (user0, cart0) := m;
        bookId !in cart && cart == cart0 - {bookId}
    ensures Inv(Normalize(Apply(m, RemoveBook(bookId))))
  {
  }
}

module F4_5Kernel refines Kernel {
  import D = F4_5Domain
}