include "Replay.dfy"

module F4_15Domain refines Domain {
  type Model = (set<string>, string, string)

  datatype Action = ViewOverview | SelectOp(opname: string) | ShowDetails

  ghost predicate Inv(m: Model) {
    m.1 == "" || m.1 in m.0
  }

  function Init(): Model {
    (set[], "", "")
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case ViewOverview => (m.0, m.1, "Overview of operations")
    case SelectOp(opname) =>
      if opname in m.0 then (m.0, opname, m.2)
      else (m.0, m.1, m.2)
    case ShowDetails =>
      if m.1 != "" then (m.0, m.1, "Details for " + m.1)
      else (m.0, m.1, m.2)
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

  lemma ViewOverviewEnsures(m: Model)
    ensures Apply(m, ViewOverview) == (m.0, m.1, "Overview of operations")
  {
  }
}

module F4_15Kernel refines Kernel {
  import D = F4_15Domain
}