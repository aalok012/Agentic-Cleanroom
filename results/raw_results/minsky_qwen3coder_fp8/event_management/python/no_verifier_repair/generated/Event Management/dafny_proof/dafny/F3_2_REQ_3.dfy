include "Replay.dfy"

module F3_2_REQ_3Domain refines Domain {
  type Model = (string, map<string, string>)

  datatype Action = Error(msg: string)

  ghost predicate Inv(m: Model) {
    var (errorMsg, _) := m;
    errorMsg == "" || errorMsg != ""
  }

  function Init(): Model {
    ("", map[])
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case Error(msg) => (msg, map[])
    }
  }

  function Normalize(m: Model): Model {
    var (errorMsg, data) := m;
    if errorMsg == "" then (errorMsg, data) else (errorMsg, data)
  }

  lemma InitSatisfiesInv()
    ensures Inv(Init())
  {
  }

  lemma StepPreservesInv(m: Model, a: Action)
    ensures Inv(Normalize(Apply(m, a)))
  {
  }

  lemma ErrorDisplaysMessage(m: Model, a: Action)
    requires a == Error("test error")
    ensures var (errorMsg, _) := Normalize(Apply(m, a)); errorMsg == "test error"
  {
  }
}

module F3_2_REQ_3Kernel refines Kernel {
  import D = F3_2_REQ_3Domain
}