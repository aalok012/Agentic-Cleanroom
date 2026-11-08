include "Replay.dfy"

module F4_8Domain refines Domain {
  type Model = (string, int, string, string, string, string, string, string, string, string)

  datatype Action =
    | ReqPrint
    | EnterDriveUrl
    | ShowCost
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
    case ReqPrint =>
      (user, 1, driveUrl, cost, deliveryInfo, paymentInfo, deliveryStatus, "", "", "")
    case EnterDriveUrl =>
      (user, 2, driveUrl, cost, deliveryInfo, paymentInfo, deliveryStatus, "", "", "")
    case ShowCost =>
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
    else m
  }

  lemma InitSatisfiesInv()
    ensures Inv(Init())
  {
  }

  lemma StepPreservesInv(m: Model, a: Action)
    ensures Inv(Normalize(Apply(m, a)))
  {
  }

  lemma ReqPrintEnsures(m: Model)
    ensures match Apply(m, ReqPrint)
      case (user, 1, _, _, _, _, _, _, _, _) => true
      case _ => false
    ensures Inv(Normalize(Apply(m, ReqPrint)))
  {
  }

  lemma EnterDriveUrlEnsures(m: Model)
    ensures match Apply(m, EnterDriveUrl)
      case (user, 2, _, _, _, _, _, _, _, _) => true
      case _ => false
    ensures Inv(Normalize(Apply(m, EnterDriveUrl)))
  {
  }

  lemma ShowCostEnsures(m: Model)
    ensures match Apply(m, ShowCost)
      case (user, 3, _, _, _, _, _, _, _, _) => true
      case _ => false
    ensures Inv(Normalize(Apply(m, ShowCost)))
  {
  }

  lemma EnterDeliveryInfoEnsures(m: Model)
    ensures match Apply(m, EnterDeliveryInfo)
      case (user, 4, _, _, _, _, _, _, _, _) => true
      case _ => false
    ensures Inv(Normalize(Apply(m, EnterDeliveryInfo)))
  {
  }

  lemma EnterPaymentInfoEnsures(m: Model)
    ensures match Apply(m, EnterPaymentInfo)
      case (user, 5, _, _, _, _, _, _, _, _) => true
      case _ => false
    ensures Inv(Normalize(Apply(m, EnterPaymentInfo)))
  {
  }

  lemma ShowDeliveryStatusEnsures(m: Model)
    ensures match Apply(m, ShowDeliveryStatus)
      case (user, 6, _, _, _, _, _, _, _, _) => true
      case _ => false
    ensures Inv(Normalize(Apply(m, ShowDeliveryStatus)))
  {
  }
}

module F4_8Kernel refines Kernel {
  import D = F4_8Domain
}