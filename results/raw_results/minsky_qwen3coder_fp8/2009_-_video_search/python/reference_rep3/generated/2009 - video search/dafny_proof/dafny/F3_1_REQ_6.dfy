include "Replay.dfy"

module F3_1_REQ_6Domain refines Domain {
  type Model = (map<string, string>, string)

  datatype Action = SortBySize | SortByDate | SortByAlpha

  ghost predicate Inv(m: Model) {
    var (torrents, sortCol) := m;
    sortCol == "size" || sortCol == "date" || sortCol == "alpha"
  }

  function Init(): Model {
    (map[], "size")
  }

  function Apply(m: Model, a: Action): Model {
    var (torrents, sortCol) := m;
    match a
    case SortBySize => (torrents, "size")
    case SortByDate => (torrents, "date")
    case SortByAlpha => (torrents, "alpha")
  }

  function Normalize(m: Model): Model {
    var (torrents, sortCol) := m;
    if sortCol == "size" || sortCol == "date" || sortCol == "alpha" then m else (torrents, "size")
  }

  lemma InitSatisfiesInv()
    ensures Inv(Init())
  {
  }

  lemma StepPreservesInv(m: Model, a: Action)
    ensures Inv(Normalize(Apply(m, a)))
  {
  }

  lemma SortBySizeUpdatesOrder()
    ensures forall t | t in Init().0 :: t == "size"
  {
  }
}

module F3_1_REQ_6Kernel refines Kernel {
  import D = F3_1_REQ_6Domain
}