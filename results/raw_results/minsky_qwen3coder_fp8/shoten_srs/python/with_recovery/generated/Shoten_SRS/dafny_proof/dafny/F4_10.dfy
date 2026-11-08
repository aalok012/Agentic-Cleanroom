include "Replay.dfy"

module F4_10Domain refines Domain {
  type Model = map<string, string>

  datatype Action = ViewContactMethods | ViewSellerDetails | ViewMap

  ghost predicate Inv(m: Model) {
    m != map[]
  }

  function Init(): Model {
    map[]
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case ViewContactMethods => m + ["contact_methods" := "bookstore, printstore, student"]
    case ViewSellerDetails => m + ["seller_details" := "address, phone, email, directions"]
    case ViewMap => m + ["map" := "locations of bookstores and printing stores"]
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

  lemma ContactMethodsAccurate(m: Model)
    ensures (m["contact_methods"] == "bookstore, printstore, student") ==> Inv(m)
  {
  }
}

module F4_10Kernel refines Kernel {
  import D = F4_10Domain
}