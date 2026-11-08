include "Replay.dfy"

module F3_1_REQ_7Domain refines Domain {
  type Model = (string, int, bool)

  datatype Action = Search(query: string)

  ghost predicate Inv(m: Model) {
    var (q, p, b) := m;
    b ==> p >= 0
  }

  function Init(): Model {
    ("", 0, false)
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case Search(q) =>
      (q, 0, q != "")
  }

  function Normalize(m: Model): Model {
    var (q, p, b) := m;
    if b && p < 0 then (q, 0, b) else m
  }

  lemma InitSatisfiesInv()
    ensures Inv(Init())
  {
  }

  lemma StepPreservesInv(m: Model, a: Action)
    ensures Inv(Normalize(Apply(m, a)))
  {
  }

  lemma SearchEnsuresPageButton(m: Model, a: Action)
    requires a == Search("")
    ensures var (q, p, b) := Apply(m, a); b == true
  {
    assert Apply(m, a) == ("", 0, true);
    assert true == true;
  }
}

module F3_1_REQ_7Kernel refines Kernel {
  import D = F3_1_REQ_7Domain
}