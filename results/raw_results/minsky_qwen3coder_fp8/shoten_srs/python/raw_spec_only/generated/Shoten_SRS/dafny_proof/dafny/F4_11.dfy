include "Replay.dfy"

module F4_11Domain refines Domain {
  type Model = (string, string, string, string, string)

  datatype Action = UpdateName(name: string)
                  | UpdateAddress(address: string)
                  | UpdateBillingAddress(billingAddress: string)
                  | UpdatePaymentInfo(paymentInfo: string)
                  | ChangePassword(oldPassword: string, newPassword: string)

  ghost predicate Inv(m: Model) {
    m.0 != "" && m.4 != ""
  }

  function Init(): Model {
    ("", "", "", "", "")
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case UpdateName(name) => (name, m.1, m.2, m.3, m.4)
    case UpdateAddress(address) => (m.0, address, m.2, m.3, m.4)
    case UpdateBillingAddress(billingAddress) => (m.0, m.1, billingAddress, m.3, m.4)
    case UpdatePaymentInfo(paymentInfo) => (m.0, m.1, m.2, paymentInfo, m.4)
    case ChangePassword(oldPassword, newPassword) => (m.0, m.1, m.2, m.3, newPassword)
  }

  function Normalize(m: Model): Model {
    if m.0 == "" || m.4 == "" then
      (if m.0 == "" then "Anonymous" else m.0,
       m.1,
       m.2,
       m.3,
       if m.4 == "" then "default_password" else m.4)
    else
      m
  }

  lemma InitSatisfiesInv()
    ensures Inv(Init())
  {
    assert Inv(("", "", "", "", ""));
  }

  lemma StepPreservesInv(m: Model, a: Action)
    ensures Inv(Normalize(Apply(m, a)))
  {
    assert true;
  }

  lemma NameUpdated(m: Model, name: string)
    ensures Apply(m, UpdateName(name)).0 == name
  {
  }

  lemma AddressUpdated(m: Model, address: string)
    ensures Apply(m, UpdateAddress(address)).1 == address
  {
  }

  lemma BillingAddressUpdated(m: Model, billingAddress: string)
    ensures Apply(m, UpdateBillingAddress(billingAddress)).2 == billingAddress
  {
  }

  lemma PaymentInfoUpdated(m: Model, paymentInfo: string)
    ensures Apply(m, UpdatePaymentInfo(paymentInfo)).3 == paymentInfo
  {
  }

  lemma PasswordChanged(m: Model, oldPassword: string, newPassword: string)
    ensures Apply(m, ChangePassword(oldPassword, newPassword)).4 == newPassword
  {
  }
}

module F4_11Kernel refines Kernel {
  import D = F4_11Domain
}