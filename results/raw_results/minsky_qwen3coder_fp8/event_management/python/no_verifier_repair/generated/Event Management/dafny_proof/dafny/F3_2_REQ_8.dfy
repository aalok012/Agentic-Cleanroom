include "Replay.dfy"

module F3_2_REQ_8Domain refines Domain {
  type Model = (string, bool)

  datatype Action = AccessClientData(adminId: string, clientId: string)

  ghost predicate Inv(m: Model) {
    m.0 == "admin" || m.0 == "user"
  }

  function Init(): Model {
    ("user", false)
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case AccessClientData(adminId, clientId) =>
      if m.0 == "admin" then
        (m.0, true)
      else
        m
  }

  function Normalize(m: Model): Model {
    if m.0 == "admin" then
      m
    else
      ("user", false)
  }

  lemma InitSatisfiesInv()
    ensures Inv(Init())
  {
  }

  lemma StepPreservesInv(m: Model, a: Action)
    ensures Inv(Normalize(Apply(m, a)))
  {
  }

  lemma AccessGrantedEnsuresViewAccess(m: Model, a: Action)
    requires Inv(m)
    requires a == AccessClientData("admin123", "client456")
    requires m.0 == "admin"
    ensures Normalize(Apply(m, a)).1 == true
  {
  }
}

module F3_2_REQ_8Kernel refines Kernel {
  import D = F3_2_REQ_8Domain
}