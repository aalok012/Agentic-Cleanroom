include "Replay.dfy"

module F4_9Domain refines Domain {
  datatype Action =
    StartAddBook |
    EnterBookDetails(name: string, quantity: int, lend: bool, sell: bool, isbn: string, author: string, rentPrice: int, sellPrice: int) |
    EnterPaymentDetails(bankAccount: string, ifscCode: string)

  datatype Book = Book(
    name: string,
    quantity: int,
    lend: bool,
    sell: bool,
    isbn: string,
    author: string,
    rentPrice: int,
    sellPrice: int,
    paymentInfo: PaymentInfo
  )

  datatype PaymentInfo = PaymentInfo(
    bankAccount: string,
    ifscCode: string
  )

  type Model = (bool, Book, PaymentInfo) 

  ghost predicate Inv(m: Model) {
    var (loggedIn, book, payment) := m;
    loggedIn &&
    book.name != "" && 
    book.quantity >= 0 && 
    book.isbn != "" && 
    book.author != "" &&
    book.rentPrice >= 0 &&
    book.sellPrice >= 0 &&
    payment.bankAccount != "" && 
    payment.ifscCode != ""
  }

  function Init(): Model {
    (false, Book("", 0, false, false, "", "", 0, 0, PaymentInfo("", "")), PaymentInfo("", ""))
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case StartAddBook =>
      var (loggedIn, book, payment) := m;
      (loggedIn, Book("", 0, false, false, "", "", 0, 0, PaymentInfo("", "")), payment)
    case EnterBookDetails(name, quantity, lend, sell, isbn, author, rentPrice, sellPrice) =>
      var (loggedIn, book, payment) := m;
      if book.name == "" && loggedIn then
        (loggedIn, Book(name, quantity, lend, sell, isbn, author, rentPrice, sellPrice, PaymentInfo("", "")), payment)
      else
        m
    case EnterPaymentDetails(bankAccount, ifscCode) =>
      var (loggedIn, book, payment) := m;
      if book.name != "" && payment.bankAccount == "" && loggedIn then
        (loggedIn, book, PaymentInfo(bankAccount, ifscCode))
      else
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

  lemma BookDetailsEnteredSuccessfully(m: Model, name: string, quantity: int, lend: bool, sell: bool, isbn: string, author: string, rentPrice: int, sellPrice: int)
    requires Inv(m) && m.0 == true
    ensures var (loggedIn, book, payment) := Apply(m, EnterBookDetails(name, quantity, lend, sell, isbn, author, rentPrice, sellPrice));
            loggedIn == m.0 && book.name == name && book.quantity == quantity && book.lend == lend && book.sell == sell && book.isbn == isbn && book.author == author && book.rentPrice == rentPrice && book.sellPrice == sellPrice
  {
    assert book.name == name;
    assert book.quantity == quantity;
    assert book.lend == lend;
    assert book.sell == sell;
    assert book.isbn == isbn;
    assert book.author == author;
    assert book.rentPrice == rentPrice;
    assert book.sellPrice == sellPrice;
  }

  lemma PaymentDetailsEnteredSuccessfully(m: Model, bankAccount: string, ifscCode: string)
    requires Inv(m) && m.0 == true && m.1.name != ""
    ensures var (loggedIn, book, payment) := Apply(m, EnterPaymentDetails(bankAccount, ifscCode));
            loggedIn == m.0 && book == m.1 && payment.bankAccount == bankAccount && payment.ifscCode == ifscCode
  {
    assert payment.bankAccount == bankAccount;
    assert payment.ifscCode == ifscCode;
  }
}

module F4_9Kernel refines Kernel {
  import D = F4_9Domain
}