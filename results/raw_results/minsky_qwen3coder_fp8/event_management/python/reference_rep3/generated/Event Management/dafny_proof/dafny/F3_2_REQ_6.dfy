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
        map["name" := "John Doe", "email" := "john@example.com", "password" := "***ENCRYPTED***", "ssn" := "***ENCRYPTED***"]
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
    assert forall k | k in Apply(m, a) :: k != "password" && k != "ssn";
  }

  lemma RetrieveStakeholderInfoReturnsEncryptedData(id: string)
    ensures (Apply(Init(), RetrieveStakeholderInfo(id)) == map[]) || 
            (Apply(Init(), RetrieveStakeholderInfo(id))["name"] == "John Doe" &&
             Apply(Init(), RetrieveStakeholderInfo(id))["password"] == "***ENCRYPTED***" &&
             Apply(Init(), RetrieveStakeholderInfo(id))["ssn"] == "***ENCRYPTED***")
  {
  }
}

module F3_2_REQ_6Kernel refines Kernel {
  import D = F3_2_REQ_6Domain
}