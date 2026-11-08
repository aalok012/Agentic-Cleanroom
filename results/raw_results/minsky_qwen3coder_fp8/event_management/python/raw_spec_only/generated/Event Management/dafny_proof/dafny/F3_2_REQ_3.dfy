include "Replay.dfy"

module F3_2_REQ_3Domain refines Domain {
  type Model = string

  datatype Action = InvalidInput

  ghost predicate Inv(m: Model) {
    m != ""
  }

  function Init(): Model {
    "Initial state"
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case InvalidInput => ""
  }

  function Normalize(m: Model): Model {
    if m == "" then "Error: Invalid input provided." else m
  }

  lemma InitSatisfiesInv()
    ensures Inv(Init())
  {
    assert Init() == "Initial state";
    assert Inv("Initial state");
  }

  lemma StepPreservesInv(m: Model, a: Action)
    ensures Inv(Normalize(Apply(m, a)))
  {
    assert Apply(m, a) == "";
    assert Normalize("") == "Error: Invalid input provided.";
    assert Inv("Error: Invalid input provided.");
  }

  lemma ErrorMsgProvided(m: Model, a: Action)
    ensures (a == InvalidInput) ==> (Normalize(Apply(m, a)) != "")
  {
    assert Apply(m, a) == "";
    assert Normalize("") == "Error: Invalid input provided.";
    assert "Error: Invalid input provided." != "";
  }
}

module F3_2_REQ_3Kernel refines Kernel {
  import D = F3_2_REQ_3Domain
}