include "Replay.dfy"

module F3_2_REQ_3Domain refines Domain {
  type Model = (string, map<string, string>)

  datatype Action = Error

  ghost predicate Inv(m: Model) {
    var (msg, _) := m;
    msg == "" || msg != ""
  }

  function Init(): Model {
    ("", map[])
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case Error => 
      var (_, errors) := m;
      ("Invalid input provided by user", errors)
  }

  function Normalize(m: Model): Model {
    var (msg, errors) := m;
    if msg == "" then ("", errors) else (msg, errors)
  }

  lemma InitSatisfiesInv()
    ensures Inv(Init())
  {
  }

  lemma StepPreservesInv(m: Model, a: Action)
    ensures Inv(Normalize(Apply(m, a)))
  {
  }

  lemma ErrorDisplaysMessage(m: Model)
    requires m == Init()
    ensures var (msg, _) := Normalize(Apply(m, Error)); msg != ""
  {
  }
}

module F3_2_REQ_3Kernel refines Kernel {
  import D = F3_2_REQ_3Domain
}