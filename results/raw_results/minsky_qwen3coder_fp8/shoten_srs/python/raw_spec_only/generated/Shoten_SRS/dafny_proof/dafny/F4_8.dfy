include "Replay.dfy"

module F4_8Domain refines Domain {
  type Model = (string, map<string, int>, string, string, string, string, string)

  datatype Action =
    RequestPrint |
    EnterGoogleDriveUrl |
    DisplayTotalCost |
    EnterDeliveryInfo |
    EnterPaymentInfo |
    DisplayDeliveryStatus

  ghost predicate Inv(m: Model) {
    var (user, items, driveUrl, totalCost, deliveryInfo, paymentInfo, deliveryStatus) := m;
    user != "" &&
    items != map[] &&
    (driveUrl == "" || driveUrl != "") &&
    (totalCost == "" || totalCost != "") &&
    (deliveryInfo == "" || deliveryInfo != "") &&
    (paymentInfo == "" || paymentInfo != "") &&
    deliveryStatus == ""
  }

  function Init(): Model {
    ("", map[], "", "", "", "", "")
  }

  function Apply(m: Model, a: Action): Model {
    var (user, items, driveUrl, totalCost, deliveryInfo, paymentInfo, deliveryStatus) := m;
    match a
    case RequestPrint =>
      (user, items, driveUrl, totalCost, deliveryInfo, paymentInfo, deliveryStatus)
    case EnterGoogleDriveUrl =>
      (user, items, "https://drive.google.com/file/d/...", totalCost, deliveryInfo, paymentInfo, deliveryStatus)
    case DisplayTotalCost =>
      (user, items, driveUrl, "$10.00", deliveryInfo, paymentInfo, deliveryStatus)
    case EnterDeliveryInfo =>
      (user, items, driveUrl, totalCost, "123 Main St", paymentInfo, deliveryStatus)
    case EnterPaymentInfo =>
      (user, items, driveUrl, totalCost, deliveryInfo, "Visa ending in 1234", deliveryStatus)
    case DisplayDeliveryStatus =>
      (user, items, driveUrl, totalCost, deliveryInfo, paymentInfo, "In Transit")
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

  lemma PrintRequestEnsures(m: Model)
    ensures Apply(m, RequestPrint) == m
  {
  }
}

module F4_8Kernel refines Kernel {
  import D = F4_8Domain
}