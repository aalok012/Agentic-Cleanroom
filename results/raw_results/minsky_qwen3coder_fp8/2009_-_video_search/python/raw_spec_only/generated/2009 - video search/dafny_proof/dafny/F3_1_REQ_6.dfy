include "Replay.dfy"

module F3_1_REQ_6Domain refines Domain {
  type Model = (map<string, int>, string)

  datatype Action = SortBySize | SortByDate | SortByAlphabetical

  ghost predicate Inv(m: Model) {
    var (results, sort) := m;
    sort == "size" || sort == "date" || sort == "alphabetical"
  }

  function Init(): Model {
    (map[], "size")
  }

  function Apply(m: Model, a: Action): Model {
    var (results, sort) := m;
    match a
    case SortBySize => (results, "size")
    case SortByDate => (results, "date")
    case SortByAlphabetical => (results, "alphabetical")
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

  lemma SortBySizeEnsures(m: Model)
    ensures (match Apply(m, SortBySize) {
      case (results, sort) => sort == "size"
    })
  {
  }
}

module F3_1_REQ_6Kernel refines Kernel {
  import D = F3_1_REQ_6Domain
}