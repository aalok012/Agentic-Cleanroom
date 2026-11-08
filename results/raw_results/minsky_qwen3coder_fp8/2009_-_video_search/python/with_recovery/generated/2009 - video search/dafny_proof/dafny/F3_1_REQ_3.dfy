include "Replay.dfy"

module F3_1_REQ_3Domain refines Domain {
  type Model = bool

  datatype Action = ToggleTorrentSearch

  ghost predicate Inv(m: Model) {
    true
  }

  function Init(): Model {
    false
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case ToggleTorrentSearch => !m
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

  lemma ToggleTorrentSearchEnsures(m: Model)
    ensures Apply(m, ToggleTorrentSearch) == !m
  {
  }
}

module F3_1_REQ_3Kernel refines Kernel {
  import D = F3_1_REQ_3Domain
}