include "Replay.dfy"

module F3_2_REQ_7Domain refines Domain {
  type Model = map<string, string>

  datatype Action = DataEntry | DataOrganization | DataRetrieval | DataModification | DataDeletion

  ghost predicate Inv(m: Model) {
    true
  }

  function Init(): Model {
    map[]
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case DataEntry => m
    case DataOrganization => m
    case DataRetrieval => m
    case DataModification => m
    case DataDeletion => m
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

  lemma ProgressMade(m: Model, a: Action)
    ensures |Apply(m, a)| >= |m|
  {
  }
}

module F3_2_REQ_7Kernel refines Kernel {
  import D = F3_2_REQ_7Domain
}