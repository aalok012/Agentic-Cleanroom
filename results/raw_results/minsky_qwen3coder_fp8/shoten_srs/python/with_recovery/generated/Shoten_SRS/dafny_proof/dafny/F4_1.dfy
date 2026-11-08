include "Replay.dfy"

module F4_1Domain refines Domain {
  type Model = (string, string, string, string, string, string, string, bool)

  datatype Action =
    | InitiateRegistration
    | ProvideInfo(name: string, rollNumber: string, shopId: string, mobile: string, email: string)
    | AssignUsername(username: string)
    | VerifyPassword(password: string)
    | StoreAccount

  ghost predicate Inv(m: Model) {
    var (name, rollNumber, shopId, mobile, email, username, password, stored) := m;
    name != "" && 
    (rollNumber == "" || rollNumber != "") &&
    (shopId == "" || shopId != "") &&
    mobile != "" &&
    email != "" &&
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
      var (_, _, _, _, _, _, _, stored) := m;
      (name, rollNumber, shopId, mobile, email, "", "", stored)
    case AssignUsername(username) =>
      var (name, rollNumber, shopId, mobile, email, _, password, stored) := m;
      (name, rollNumber, shopId, mobile, email, username, password, stored)
    case VerifyPassword(password) =>
      var (name, rollNumber, shopId, mobile, email, username, _, stored) := m;
      (name, rollNumber, shopId, mobile, email, username, password, stored)
    case StoreAccount =>
      var (name, rollNumber, shopId, mobile, email, username, password, _) := m;
      (name, rollNumber, shopId, mobile, email, username, password, true)
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
    match a
    case InitiateRegistration =>
    case ProvideInfo(name, rollNumber, shopId, mobile, email) =>
      assert name != "";
      assert mobile != "";
      assert email != "";
      assert rollNumber == "" || rollNumber != "";
      assert shopId == "" || shopId != "";
    case AssignUsername(username) =>
      var (name, rollNumber, shopId, mobile, email, _, password, _) := m;
      assert name != "";
      assert mobile != "";
      assert email != "";
      assert username != "";
      assert rollNumber == "" || rollNumber != "";
      assert shopId == "" || shopId != "";
      assert password == "" || password != "";
    case VerifyPassword(password) =>
      var (name, rollNumber, shopId, mobile, email, username, _, _) := m;
      assert name != "";
      assert mobile != "";
      assert email != "";
      assert username != "";
      assert rollNumber == "" || rollNumber != "";
      assert shopId == "" || shopId != "";
      assert password != "";
    case StoreAccount =>
      var (name, rollNumber, shopId, mobile, email, username, password, _) := m;
      assert name != "";
      assert mobile != "";
      assert email != "";
      assert username != "";
      assert rollNumber == "" || rollNumber != "";
      assert shopId == "" || shopId != "";
      assert password != "";
  }

  lemma InfoProvidedEnsures(m: Model, name: string, rollNumber: string, shopId: string, mobile: string, email: string)
    requires Inv(m)
    ensures Inv(Apply(m, ProvideInfo(name, rollNumber, shopId, mobile, email)))
  {
    assert name != "";
    assert mobile != "";
    assert email != "";
    assert rollNumber == "" || rollNumber != "";
    assert shopId == "" || shopId != "";
  }
}

module F4_1Kernel refines Kernel {
  import D = F4_1Domain
}