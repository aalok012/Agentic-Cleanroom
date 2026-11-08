include "Replay.dfy"

module F4_2Domain refines Domain {
  type Model = (bool, string)

  datatype Action = Login(username: string, password: string) | Prompt

  ghost predicate Inv(m: Model) {
    m.0 == true || m.0 == false
  }

  function Init(): Model {
    (false, "")
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case Login(u, p) => 
      if u == "validuser" && p == "validpass" then (true, u) else m
    case Prompt => m
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

  lemma LoginSucceeds(m: Model, u: string, p: string)
    requires m.0 == false && u == "validuser" && p == "validpass"
    ensures Apply(m, Login(u, p)).0 == true
  {
  }
}

module F4_2Kernel refines Kernel {
  import D = F4_2Domain
}