include "Replay.dfy"

module F4_12Domain refines Domain {
  type Model = (map<string, Order>, string)

  datatype Action = ViewRecentOrders(user: string)
                  | ViewOrderById(confNum: string)
                  | ViewOrderDetails(orderId: string)

  datatype OrderStatus = InTransit | Delivered | Processing

  datatype Order = Order(
    id: string,
    userId: string,
    shippingDate: int,
    mailingAddress: string,
    projectedDeliveryDate: int,
    status: OrderStatus
  )

  ghost predicate Inv(m: Model) {
    var (orders, currentUser) := m;
    forall o | o in orders :: 
      o.userId == currentUser && o.shippingDate >= 0 && o.projectedDeliveryDate >= o.shippingDate
  }

  function Init(): Model {
    (map[], "")
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case ViewRecentOrders(user) => (m.0, user)
    case ViewOrderById(confNum) => m
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

  lemma ViewRecentOrdersEnsures(m: Model, user: string)
    ensures (match Apply(m, ViewRecentOrders(user))
             case (_, u) => u == user)
  {
  }
}

module F4_12Kernel refines Kernel {
  import D = F4_12Domain
}