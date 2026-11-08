include "Replay.dfy"

module F4_2Domain refines Domain {
  type Model = (string, bool)

  datatype Action = Login(username: string, password: string)

  ghost predicate Inv(m: Model) {
    var (user, logged_in) := m;
    logged_in ==> user != ""
  }

  function Init(): Model {
    ("", false)
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case Login(user, pass) =>
      if user != "" && pass != "" then
        (user, true)
      else
        m
  }

  function Normalize(m: Model): Model {
    var (user, logged_in) := m;
    if logged_in && user == "" then
      ("", false)
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

  lemma LoginEnsuresLoggedIn(m: Model, a: Action)
    requires a == Login("user123", "pass456")
    ensures var (user, logged_in) := Normalize(Apply(m, a)); logged_in
  {
    assert Apply(m, a) == ("user123", true);
    assert Normalize(("user123", true)) == ("user123", true);
  }
}

module F4_2Kernel refines Kernel {
  import D = F4_2Domain
}