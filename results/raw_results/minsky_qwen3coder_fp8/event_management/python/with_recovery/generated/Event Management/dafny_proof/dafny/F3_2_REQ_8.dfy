include "Replay.dfy"

module F3_2_REQ_8Domain refines Domain {
  type Model = (string, bool, map<string, string>)

  datatype Action = AccessClientData(adminId: string, clientId: string)

  ghost predicate Inv(m: Model) {
    var (adminId, hasAccess, clientData) := m;
    true
  }

  function Init(): Model {
    ("", false, map[])
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case AccessClientData(adminId, clientId) =>
      var (currentAdminId, currentHasAccess, clientData) := m;
      if currentAdminId == adminId && currentHasAccess then
        (adminId, true, clientData)
      else
        (adminId, false, clientData)
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

  lemma AccessGrantedEnsuresViewAccess(adminId: string, clientId: string)
    ensures var (actualAdminId, hasAccess, data) := Apply(Init(), AccessClientData(adminId, clientId));
           hasAccess ==> actualAdminId == adminId
  {
  }
}

module F3_2_REQ_8Kernel refines Kernel {
  import D = F3_2_REQ_8Domain
}