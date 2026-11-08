include "Replay.dfy"

module F4_11Domain refines Domain {
  type Model = (string, string, string, string, string, string)

  datatype Action =
    | UpdateAccountInfo(name: string, mailingAddr: string, billingAddr: string, paymentInfo: string)
    | ChangePassword(oldPass: string, newPass1: string, newPass2: string)

  ghost predicate Inv(m: Model) {
    var (name, mailAddr, billAddr, payInfo, oldPass, newPass) := m;
    true  // No additional constraints specified
  }

  function Init(): Model {
    ("", "", "", "", "", "")
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case UpdateAccountInfo(name, mailingAddr, billingAddr, paymentInfo) =>
      var (oldName, oldMailAddr, oldBillAddr, oldPayInfo, oldPass, newPass) := m;
      (name, mailingAddr, billingAddr, paymentInfo, oldPass, newPass)
    case ChangePassword(oldPass, newPass1, newPass2) =>
      var (name, mailAddr, billAddr, payInfo, oldPassStored, newPassStored) := m;
      if oldPass == oldPassStored && newPass1 == newPass2 then
        (name, mailAddr, billAddr, payInfo, oldPass, newPass1)
      else
        m
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

  lemma UpdateAccountInfoEnsures(m: Model, name: string, mailingAddr: string, billingAddr: string, paymentInfo: string)
    ensures Apply(m, UpdateAccountInfo(name, mailingAddr, billingAddr, paymentInfo)) == (name, mailingAddr, billingAddr, paymentInfo, m.5, m.6)
  {
  }

  lemma ChangePasswordEnsures(m: Model, oldPass: string, newPass1: string, newPass2: string)
    requires oldPass == m.5 && newPass1 == newPass2
    ensures Apply(m, ChangePassword(oldPass, newPass1, newPass2)) == (m.1, m.2, m.3, m.4, oldPass, newPass1)
  {
  }
}

module F4_11Kernel refines Kernel {
  import D = F4_11Domain
}