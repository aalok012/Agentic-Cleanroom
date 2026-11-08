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

  type Model = (bool, option<Book>, option<PaymentInfo>)

  ghost predicate Inv(m: Model) {
    var (loggedIn, bookOpt, paymentOpt) := m;
    loggedIn &&
    (bookOpt == none || 
      (bookOpt != none && 
       var book := bookOpt.get;
       book.name != "" && 
       book.quantity >= 0 && 
       book.isbn != "" && 
       book.author != "" &&
       book.rentPrice >= 0 &&
       book.sellPrice >= 0)) &&
    (paymentOpt == none || 
      (paymentOpt != none && 
       var payment := paymentOpt.get;
       payment.bankAccount != "" && 
       payment.ifscCode != ""))
  }

  function Init(): Model {
    (false, none, none)
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case StartAddBook =>
      var (loggedIn, bookOpt, paymentOpt) := m;
      (loggedIn, none, none)
    case EnterBookDetails(name, quantity, lend, sell, isbn, author, rentPrice, sellPrice) =>
      var (loggedIn, bookOpt, paymentOpt) := m;
      if bookOpt == none && loggedIn then
        (loggedIn, some(Book(name, quantity, lend, sell, isbn, author, rentPrice, sellPrice, PaymentInfo("", ""))), paymentOpt)
      else
        m
    case EnterPaymentDetails(bankAccount, ifscCode) =>
      var (loggedIn, bookOpt, paymentOpt) := m;
      if bookOpt != none && paymentOpt == none && loggedIn then
        (loggedIn, bookOpt, some(PaymentInfo(bankAccount, ifscCode)))
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
    ensures var (loggedIn, bookOpt, paymentOpt) := Apply(m, EnterBookDetails(name, quantity, lend, sell, isbn, author, rentPrice, sellPrice));
            loggedIn == m.0 && bookOpt != none && bookOpt.get.name == name && bookOpt.get.quantity == quantity && bookOpt.get.lend == lend && bookOpt.get.sell == sell && bookOpt.get.isbn == isbn && bookOpt.get.author == author && bookOpt.get.rentPrice == rentPrice && bookOpt.get.sellPrice == sellPrice
  {
  }

  lemma PaymentDetailsEnteredSuccessfully(m: Model, bankAccount: string, ifscCode: string)
    requires Inv(m) && m.0 == true && m.1 != none
    ensures var (loggedIn, bookOpt, paymentOpt) := Apply(m, EnterPaymentDetails(bankAccount, ifscCode));
            loggedIn == m.0 && bookOpt == m.1 && paymentOpt != none && paymentOpt.get.bankAccount == bankAccount && paymentOpt.get.ifscCode == ifscCode
  {
  }
}

module F4_9Kernel refines Kernel {
  import D = F4_9Domain
}