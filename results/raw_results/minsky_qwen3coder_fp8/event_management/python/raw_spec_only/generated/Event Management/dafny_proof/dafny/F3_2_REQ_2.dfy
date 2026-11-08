include "Replay.dfy"

module F3_2_REQ_2Domain refines Domain {
  type Model = map<string, set<string>>

  datatype Action = Register(student: string, event: string)

  ghost predicate Inv(m: Model) {
    forall s | s in m ==> m[s] == set[]
  }

  function Init(): Model {
    map[]
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case Register(s, e) => m[s := m[s] + {e}]
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

  lemma RegisterEnsures(m: Model, s: string, e: string)
    ensures Inv(m[s := m[s] + {e}])
  {
  }
}

module F3_2_REQ_2Kernel refines Kernel {
  import D = F3_2_REQ_2Domain
}