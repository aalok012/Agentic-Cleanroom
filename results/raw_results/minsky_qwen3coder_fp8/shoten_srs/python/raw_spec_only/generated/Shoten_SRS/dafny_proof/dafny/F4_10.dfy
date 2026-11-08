include "Replay.dfy"

module F4_10Domain refines Domain {
  type Model = (string, string, string, string, string, string, string, string, string, string, string, string)

  datatype Action = ViewContactInfo | DisplayStoreDetails | ShowMap

  ghost predicate Inv(m: Model) {
    var (bookstoreAddr, bookstorePhone, bookstoreEmail, printstoreAddr, printstorePhone, printstoreEmail, studentAddr, studentPhone, studentEmail, bookstoreDir, printstoreDir, studentDir) := m;
    bookstoreAddr != "" && bookstorePhone != "" && bookstoreEmail != "" &&
    printstoreAddr != "" && printstorePhone != "" && printstoreEmail != "" &&
    studentAddr != "" && studentPhone != "" && studentEmail != "" &&
    bookstoreDir != "" && printstoreDir != "" && studentDir != ""
  }

  function Init(): Model {
    ("Bookstore Address", "Bookstore Phone", "Bookstore Email",
     "Printstore Address", "Printstore Phone", "Printstore Email",
     "Student Address", "Student Phone", "Student Email",
     "Bookstore Directions", "Printstore Directions", "Student Directions")
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case ViewContactInfo =>
      var (bookstoreAddr, bookstorePhone, bookstoreEmail, printstoreAddr, printstorePhone, printstoreEmail, studentAddr, studentPhone, studentEmail, bookstoreDir, printstoreDir, studentDir) := m;
      (bookstoreAddr, bookstorePhone, bookstoreEmail, printstoreAddr, printstorePhone, printstoreEmail, studentAddr, studentPhone, studentEmail, bookstoreDir, printstoreDir, studentDir)
    case DisplayStoreDetails =>
      var (bookstoreAddr, bookstorePhone, bookstoreEmail, printstoreAddr, printstorePhone, printstoreEmail, studentAddr, studentPhone, studentEmail, bookstoreDir, printstoreDir, studentDir) := m;
      (bookstoreAddr, bookstorePhone, bookstoreEmail, printstoreAddr, printstorePhone, printstoreEmail, studentAddr, studentPhone, studentEmail, bookstoreDir, printstoreDir, studentDir)
    case ShowMap =>
      var (bookstoreAddr, bookstorePhone, bookstoreEmail, printstoreAddr, printstorePhone, printstoreEmail, studentAddr, studentPhone, studentEmail, bookstoreDir, printstoreDir, studentDir) := m;
      (bookstoreAddr, bookstorePhone, bookstoreEmail, printstoreAddr, printstorePhone, printstoreEmail, studentAddr, studentPhone, studentEmail, bookstoreDir, printstoreDir, studentDir)
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

  lemma ContactInfoDisplayed(m: Model)
    ensures m == (m.0, m.1, m.2, m.3, m.4, m.5, m.6, m.7, m.8, m.9, m.10, m.11)
  {
  }
}

module F4_10Kernel refines Kernel {
  import D = F4_10Domain
}