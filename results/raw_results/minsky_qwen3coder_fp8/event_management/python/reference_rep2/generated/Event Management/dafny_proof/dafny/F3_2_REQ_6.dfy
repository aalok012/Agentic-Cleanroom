include "Replay.dfy"

module F3_2_REQ_6Domain refines Domain {
  type Model = map<string, string>

  datatype Action = RetrieveStakeholderInfo(id: string)

  ghost predicate Inv(m: Model) {
    forall k | k in m :: k != "password" && k != "ssn"
  }

  function Init(): Model {
    map[]
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case RetrieveStakeholderInfo(id) =>
      if id == "user123" then
        map["name" := "John Doe", "email" := "john@example.com", "role" := "admin"]
      else if id == "user456" then
        map["name" := "Jane Smith", "email" := "jane@example.com", "role" := "user"]
      else
        map[]
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

  lemma RetrieveStakeholderInfoEnsures(m: Model, id: string)
    ensures (match Apply(m, RetrieveStakeholderInfo(id))
      case result => 
        forall k | k in result :: k != "password" && k != "ssn"
    )
  {
  }
}

module F3_2_REQ_6Kernel refines Kernel {
  import D = F3_2_REQ_6Domain
}