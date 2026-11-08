include "Replay.dfy"

module F4_1Domain refines Domain {
  type Model = (string, string, string, string, string, string, bool)

  datatype Action = 
    InitiateRegistration |
    ProvideInfo(name: string, rollNumber: string, shopId: string, mobile: string, email: string) |
    AssignUsername(username: string) |
    VerifyPassword(password: string) |
    StoreAccount

  ghost predicate Inv(m: Model) {
    var (name, rollNumber, shopId, mobile, email, username, passwordSet) := m;
    name != "" && mobile != "" && email != "" && (rollNumber != "" || shopId != "") && (username != "" || !passwordSet)
  }

  function Init(): Model {
    ("", "", "", "", "", "", false)
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case InitiateRegistration => m
    case ProvideInfo(name, rollNumber, shopId, mobile, email) =>
      var (n, r, s, mob, e, u, p) := m;
      (name, rollNumber, shopId, mobile, email, u, p)
    case AssignUsername(username) =>
      var (n, r, s, mob, e, u, p) := m;
      (n, r, s, mob, e, username, p)
    case VerifyPassword(password) =>
      var (n, r, s, mob, e, u, p) := m;
      (n, r, s, mob, e, u, true)
    case StoreAccount =>
      m
  }

  function Normalize(m: Model): Model {
    m
  }

  lemma InitSatisfiesInv()
    ensures Inv(Init())
  {
    assert Inv(("","", "", "", "", "", false));
  }

  lemma StepPreservesInv(m: Model, a: Action)
    ensures Inv(Normalize(Apply(m, a)))
  {
    var applied := Apply(m, a);
    var normalized := Normalize(applied);
    match a
    case InitiateRegistration =>
      assert Inv(normalized);
    case ProvideInfo(name, rollNumber, shopId, mobile, email) =>
      assert name != "";
      assert mobile != "";
      assert email != "";
      assert (rollNumber != "" || shopId != "");
      assert Inv(normalized);
    case AssignUsername(username) =>
      assert username != "";
      assert Inv(normalized);
    case VerifyPassword(password) =>
      assert Inv(normalized);
    case StoreAccount =>
      assert Inv(normalized);
  }

  lemma PostconditionFR41REQ1(m: Model, a: Action)
    requires Inv(m)
    requires a == InitiateRegistration
    ensures var (name, rollNumber, shopId, mobile, email, username, passwordSet) := Apply(m, a); name == "" && rollNumber == "" && shopId == "" && mobile == "" && email == "" && username == "" && passwordSet == false
  {
    assert Apply(m, a) == m;
  }
}

module F4_1Kernel refines Kernel {
  import D = F4_1Domain
}