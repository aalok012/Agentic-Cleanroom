include "Replay.dfy"

module F4_8Domain refines Domain {
  type Model = (string, int, string, string, string, string, string, string, string, string)

  datatype Action =
    | PrintRequested
    | EnterGoogleDriveUrl
    | ShowTotalCost
    | EnterDeliveryInfo
    | EnterPaymentInfo
    | ShowDeliveryStatus

  ghost predicate Inv(m: Model) {
    var (user, step, driveUrl, cost, deliveryInfo, paymentInfo, deliveryStatus, _, _, _) := m;
    step >= 0 && step <= 6
  }

  function Init(): Model {
    ("", 0, "", "", "", "", "", "", "", "")
  }

  function Apply(m: Model, a: Action): Model {
    var (user, step, driveUrl, cost, deliveryInfo, paymentInfo, deliveryStatus, _, _, _) := m;
    match a
    case PrintRequested =>
      (user, 1, driveUrl, cost, deliveryInfo, paymentInfo, deliveryStatus, "", "", "")
    case EnterGoogleDriveUrl =>
      (user, 2, driveUrl, cost, deliveryInfo, paymentInfo, deliveryStatus, "", "", "")
    case ShowTotalCost =>
      (user, 3, driveUrl, cost, deliveryInfo, paymentInfo, deliveryStatus, "", "", "")
    case EnterDeliveryInfo =>
      (user, 4, driveUrl, cost, deliveryInfo, paymentInfo, deliveryStatus, "", "", "")
    case EnterPaymentInfo =>
      (user, 5, driveUrl, cost, deliveryInfo, paymentInfo, deliveryStatus, "", "", "")
    case ShowDeliveryStatus =>
      (user, 6, driveUrl, cost, deliveryInfo, paymentInfo, deliveryStatus, "", "", "")
  }

  function Normalize(m: Model): Model {
    var (user, step, driveUrl, cost, deliveryInfo, paymentInfo, deliveryStatus, _, _, _) := m;
    if step < 0 then (user, 0, driveUrl, cost, deliveryInfo, paymentInfo, deliveryStatus, "", "", "")
    else if step > 6 then (user, 6, driveUrl, cost, deliveryInfo, paymentInfo, deliveryStatus, "", "", "")
    else (user, step, driveUrl, cost, deliveryInfo, paymentInfo, deliveryStatus, "", "", "")
  }

  lemma InitSatisfiesInv()
    ensures Inv(Init())
  {
  }

  lemma StepPreservesInv(m: Model, a: Action)
    ensures Inv(Normalize(Apply(m, a)))
  {
  }

  lemma PrintRequestedEnsures(m: Model)
    ensures Inv(Normalize(Apply(m, PrintRequested)))
  {
  }

  lemma EnterGoogleDriveUrlEnsures(m: Model)
    ensures Inv(Normalize(Apply(m, EnterGoogleDriveUrl)))
  {
  }

  lemma ShowTotalCostEnsures(m: Model)
    ensures Inv(Normalize(Apply(m, ShowTotalCost)))
  {
  }

  lemma EnterDeliveryInfoEnsures(m: Model)
    ensures Inv(Normalize(Apply(m, EnterDeliveryInfo)))
  {
  }

  lemma EnterPaymentInfoEnsures(m: Model)
    ensures Inv(Normalize(Apply(m, EnterPaymentInfo)))
  {
  }

  lemma ShowDeliveryStatusEnsures(m: Model)
    ensures Inv(Normalize(Apply(m, ShowDeliveryStatus)))
  {
  }
}

module F4_8Kernel refines Kernel {
  import D = F4_8Domain
}