include "Replay.dfy"

module F4_12Domain refines Domain {
  type Model = (map<string, Order>, string)

  datatype Action = ViewOrders | ViewByConfirmation(conf: string) | ViewOrderDetails(orderId: string)

  datatype OrderStatus = InTransit | Delivered

  datatype Order = Order(
    id: string,
    userId: string,
    shippingDate: int,
    mailingAddress: string,
    projectedDeliveryDate: int,
    status: OrderStatus
  )

  ghost predicate Inv(m: Model) {
    var (orders, user) := m;
    forall id | id in orders :: 
      orders[id].userId == user &&
      orders[id].shippingDate >= 0 &&
      orders[id].projectedDeliveryDate >= orders[id].shippingDate
  }

  function Init(): Model {
    (map[], "")
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case ViewOrders => m
    case ViewByConfirmation(conf) => m
    case ViewOrderDetails(orderId) => m
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

  lemma ViewOrdersEnsures(m: Model)
    ensures forall id | id in m.0 && m.0[id].userId == m.1 ::
      m.0[id].shippingDate >= 0 &&
      m.0[id].projectedDeliveryDate >= m.0[id].shippingDate
  {
    // The invariant already establishes this property
    assert forall id | id in m.0 && m.0[id].userId == m.1 ::
      m.0[id].shippingDate >= 0 &&
      m.0[id].projectedDeliveryDate >= m.0[id].shippingDate;
  }
}

module F4_12Kernel refines Kernel {
  import D = F4_12Domain
}