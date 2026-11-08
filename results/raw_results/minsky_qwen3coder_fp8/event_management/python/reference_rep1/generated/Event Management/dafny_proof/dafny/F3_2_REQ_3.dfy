include "Replay.dfy"

module F3_2_REQ_3Domain refines Domain {
  type Model = (string, bool)

  datatype Action = Error

  ghost predicate Inv(m: Model) {
    m.1 == false || m.0 == ""
  }

  function Init(): Model {
    ("", false)
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case Error => ("error occurred", true)
  }

  function Normalize(m: Model): Model {
    if m.1 then ("", false) else m
  }

  lemma InitSatisfiesInv()
    ensures Inv(Init())
  {
  }

  lemma StepPreservesInv(m: Model, a: Action)
    ensures Inv(Normalize(Apply(m, a)))
  {
    if a == Error {
      assert Normalize(Apply(m, a)) == ("", false);
      assert Inv(("", false));
    }
  }

  lemma ErrorDisplaysMessage(m: Model)
    requires m.1 == false
    ensures (Normalize(Apply(m, Error))).0 != ""
  {
    assert Normalize(Apply(m, Error)) == ("", false);
    assert ("", false).0 == "";
    assert false;
  }
}

module F3_2_REQ_3Kernel refines Kernel {
  import D = F3_2_REQ_3Domain
}