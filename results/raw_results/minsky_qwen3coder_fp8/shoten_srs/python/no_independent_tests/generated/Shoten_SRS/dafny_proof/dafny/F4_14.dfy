include "Replay.dfy"

module F4_14Domain refines Domain {
  type Model = (bool, map<string, string>)

  datatype Action = Logout

  ghost predicate Inv(m: Model) {
    var (logged_in, tokens) := m;
    logged_in ==> tokens != map[]
  }

  function Init(): Model {
    (false, map[])
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case Logout => (false, map[])
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

  lemma LogoutInvalidatesToken(m: Model)
    ensures (match Apply(m, Logout) {
      case (false, _) => true
      case _ => false
    })
  {
  }
}

module F4_14Kernel refines Kernel {
  import D = F4_14Domain
}