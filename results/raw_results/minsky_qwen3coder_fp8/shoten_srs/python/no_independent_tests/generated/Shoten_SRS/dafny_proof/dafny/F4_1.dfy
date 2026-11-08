include "Replay.dfy"

module F4_1Domain refines Domain {
  type Model = (string, string, string, string, string, string, string, bool)

  datatype Action = 
    InitiateRegistration |
    ProvideInfo(name: string, rollNumber: string, shopId: string, mobile: string, email: string) |
    AssignUsername(username: string) |
    ConfirmPassword(password: string) |
    StoreAccount

  ghost predicate Inv(m: Model) {
    var (name, rollNumber, shopId, mobile, email, username, password, stored) := m;
    name != "" && 
    mobile != "" && 
    email != "" &&
    (rollNumber == "" || rollNumber != "") &&
    (shopId == "" || shopId != "") &&
    (username == "" || username != "") &&
    (password == "" || password != "") &&
    stored == false
  }

  function Init(): Model {
    ("", "", "", "", "", "", "", false)
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case InitiateRegistration => m
    case ProvideInfo(name, rollNumber, shopId, mobile, email) =>
      var (n, r, s, mob, e, u, p, st) := m;
      (name, rollNumber, shopId, mobile, email, u, p, st)
    case AssignUsername(username) =>
      var (n, r, s, mob, e, u, p, st) := m;
      (n, r, s, mob, e, username, p, st)
    case ConfirmPassword(password) =>
      var (n, r, s, mob, e, u, p, st) := m;
      (n, r, s, mob, e, u, password, st)
    case StoreAccount =>
      var (n, r, s, mob, e, u, p, st) := m;
      (n, r, s, mob, e, u, p, true)
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

  lemma InfoProvidedEnsures(m: Model, name: string, rollNumber: string, shopId: string, mobile: string, email: string)
    ensures Apply(m, ProvideInfo(name, rollNumber, shopId, mobile, email)) == (name, rollNumber, shopId, mobile, email, "", "", false)
  {
  }
}

module F4_1Kernel refines Kernel {
  import D = F4_1Domain
}