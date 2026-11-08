include "Replay.dfy"

module F4_15Domain refines Domain {
  type Model = (set<string>, string, string)

  datatype Action = ViewOverview | SelectOp(opname: string) | ShowDetails

  ghost predicate Inv(m: Model) {
    var (ops, selected, details) := m;
    selected == "" || selected in ops
  }

  function Init(): Model {
    (set[], "", "")
  }

  function Apply(m: Model, a: Action): Model {
    var (ops, selected, details) := m;
    match a
    case ViewOverview => (ops, selected, "Overview of operations")
    case SelectOp(opname) =>
      if opname in ops then (ops, opname, details)
      else (ops, selected, details)
    case ShowDetails =>
      if selected != "" then (ops, selected, "Details for " + selected)
      else (ops, selected, details)
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

  lemma SelectOpEnsures(m: Model, opname: string)
    ensures Apply(m, SelectOp(opname)) == (m.0, if opname in m.0 then opname else m.1, m.2)
  {
  }

  lemma ShowDetailsEnsures(m: Model)
    ensures Apply(m, ShowDetails) == (m.0, m.1, if m.1 != "" then "Details for " + m.1 else m.2)
  {
  }
}

module F4_15Kernel refines Kernel {
  import D = F4_15Domain
}