include "Replay.dfy"

module F4_14Domain refines Domain {
  type Model = (bool, string)

  datatype Action = Logout

  ghost predicate Inv(m: Model) {
    match m
    case (loggedIn, _) => loggedIn == false
  }

  function Init(): Model {
    (false, "")
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case Logout => (false, "")
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

  lemma LogoutDisablesLogin()
    ensures forall m: Model, a: Action :: Inv(m) ==> Inv(Normalize(Apply(m, a)))
  {
  }
}

module F4_14Kernel refines Kernel {
  import D = F4_14Domain
}