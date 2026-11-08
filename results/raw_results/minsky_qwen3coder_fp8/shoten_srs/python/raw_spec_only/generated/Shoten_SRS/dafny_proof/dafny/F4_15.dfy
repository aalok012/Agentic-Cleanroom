include "Replay.dfy"

module F4_15Domain refines Domain {
  type Model = (string, map<string, string>)

  datatype Action = ViewHelp | SelectOp(op: string) | ShowOpHelp(op: string)

  ghost predicate Inv(m: Model) {
    var (overview, ops) := m;
    overview == "" || overview == "help overview"
  }

  function Init(): Model {
    ("", map[])
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case ViewHelp => ("help overview", m.1)
    case SelectOp(op) => (m.0, m.1)
    case ShowOpHelp(op) => (m.0, m.1)
  }

  function Normalize(m: Model): Model {
    var (overview, ops) := m;
    if overview == "" then ("help overview", ops) else (overview, ops)
  }

  lemma InitSatisfiesInv()
    ensures Inv(Init())
  {
  }

  lemma StepPreservesInv(m: Model, a: Action)
    ensures Inv(Normalize(Apply(m, a)))
  {
  }

  lemma ViewHelpEnsuresOverview(m: Model)
    ensures (match Apply(m, ViewHelp)
             case (overview, ops) => overview == "help overview"
           )
  {
  }
}

module F4_15Kernel refines Kernel {
  import D = F4_15Domain
}