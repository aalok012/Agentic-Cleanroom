include "Replay.dfy"

module F4_1Domain refines Domain {
  datatype Action = RegisterUser(name: string, rollNumber: string, shopId: string, mobile: string, email: string, username: string, password: string)

  type Model = map<string, (string, string, string, string, string, string)]

  ghost predicate Inv(m: Model) {
    forall k | k in m :: m[k].Item6 == k
  }

  function Init(): Model {
    map[]
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case RegisterUser(name, rollNumber, shopId, mobile, email, username, password) =>
      m[username := (name, rollNumber, shopId, mobile, email, username)]
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

  lemma RegisterUserEnsures(m: Model, a: Action)
    requires a == RegisterUser("John Doe", "12345", "", "9876543210", "john@example.com", "johndoe", "password123")
    ensures forall k | k in Apply(m, a) :: (Apply(m, a)[k].Item6 == k)
  {
  }
}

module F4_1Kernel refines Kernel {
  import D = F4_1Domain
}