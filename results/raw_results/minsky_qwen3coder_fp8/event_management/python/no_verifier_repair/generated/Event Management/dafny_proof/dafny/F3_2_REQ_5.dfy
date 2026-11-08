include "Replay.dfy"

module F3_2_REQ_5Domain refines Domain {
  type Model = map<string, string>

  datatype Action = GetRegistrants

  ghost predicate Inv(m: Model) {
    true
  }

  function Init(): Model {
    map[]
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case GetRegistrants => m
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

  lemma GetRegistrantsEnsures(m: Model)
    ensures Apply(m, GetRegistrants) == m
  {
  }
}

module F3_2_REQ_5Kernel refines Kernel {
  import D = F3_2_REQ_5Domain
}