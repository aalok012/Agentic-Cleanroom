include "Replay.dfy"

module F3_2_REQ_12Domain refines Domain {
  type Model = string

  datatype Action = SetStimulus(stimulus: string)

  ghost predicate Inv(m: Model) {
    m == ""
  }

  function Init(): Model {
    ""
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case SetStimulus(s) => s
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

  lemma SetStimulusEnsuresEmpty(m: Model, s: string)
    ensures Apply(m, SetStimulus(s)) == s
  {
  }
}

module F3_2_REQ_12Kernel refines Kernel {
  import D = F3_2_REQ_12Domain
}