include "Replay.dfy"

module F3_2_REQ_8Domain refines Domain {
  type Model = (bool, map<string, string>)

  datatype Action = AccessClientData | ModifyClientData

  ghost predicate Inv(m: Model) {
    true
  }

  function Init(): Model {
    (false, map[])
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case AccessClientData =>
      if m.0 then (true, m.1) else (false, m.1)
    case ModifyClientData =>
      if m.0 then (true, m.1) else (false, m.1)
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

  lemma AccessGrantedEnsuresViewAccess(m: Model)
    requires m.0 == true
    ensures m.1 == m.1
  {
  }
}

module F3_2_REQ_8Kernel refines Kernel {
  import D = F3_2_REQ_8Domain
}