include "Replay.dfy"

module F4_12Domain refines Domain {
  type Model = (map<string, OrderInfo>, set<string>)

  datatype Action = ViewStatus(confNum: string)

  datatype OrderStatus = InTransit | Delivered

  record OrderInfo = {
    orderDate: string,
    shippingDate: string,
    mailingAddress: string,
    projectedDeliveryDate: string,
    status: OrderStatus
  }

  ghost predicate Inv(m: Model) {
    m.1 == set k | k in m.0 && m.0[k].orderDate != "" :: k
  }

  function Init(): Model {
    (map[], {})
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case ViewStatus(confNum) => m
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

  lemma ViewStatusEnsures(m: Model, confNum: string)
    ensures (if confNum in m.0 && confNum in m.1 then
      m.0[confNum].shippingDate != "" && 
      m.0[confNum].mailingAddress != "" && 
      m.0[confNum].projectedDeliveryDate != "" &&
      (m.0[confNum].status == InTransit || m.0[confNum].status == Delivered)
    else
      true)
  {
  }
}

module F4_12Kernel refines Kernel {
  import D = F4_12Domain
}