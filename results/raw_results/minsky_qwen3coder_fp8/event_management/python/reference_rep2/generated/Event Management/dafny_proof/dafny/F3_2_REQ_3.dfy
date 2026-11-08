include "Replay.dfy"

module F3_2_REQ_3Domain refines Domain {
  type Model = (string, bool)

  datatype Action = Error

  ghost predicate Inv(m: Model) {
    var (msg, shown) := m;
    true
  }

  function Init(): Model {
    ("", false)
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case Error => ("Invalid input provided by user", true)
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

  lemma ErrorDisplaysMessage(m: Model)
    requires Inv(m)
    ensures var (msg, shown) := Normalize(Apply(m, Error)); msg != "" && shown
  {
  }
}

module F3_2_REQ_3Kernel refines Kernel {
  import D = F3_2_REQ_3Domain
}