include "Replay.dfy"

module F4_6Domain refines Domain {
  datatype Action =
    | InitiateRent
    | EnterRentalPeriod(period: int)
    | ConfirmRentalPeriod
    | EnterDeliveryInfo(address: string, contact: string)
    | EnterPaymentInfo(payment: string)
    | CompleteTransaction

  datatype RentalState = 
    | NotStarted
    | CartSelected
    | PeriodEntered
    | DeliveryInfoEntered
    | PaymentInfoEntered
    | TransactionComplete

  datatype BookInfo = 
    | Book(title: string, price: int, quantity: int)

  datatype Cart = 
    | Cart(items: map<string, BookInfo>)

  datatype RentalDetailsInfo = 
    | RentalDetails(period: int, totalAmount: int, individualAmounts: map<string, int>)

  datatype UserInfo = 
    | User(id: string, name: string, isLoggedIn: bool)

  datatype DeliveryInfoData = 
    | DeliveryInfo(address: string, contact: string)

  datatype PaymentInfoData = 
    | PaymentInfo(method: string)

  datatype TransactionInfo = 
    | Transaction(rentedBooks: map<string, BookInfo>, deliveryInfo: DeliveryInfoData, paymentInfo: PaymentInfoData)

  datatype AppState = 
    | AppState(
        user: UserInfo,
        cart: Cart,
        rentalState: RentalState,
        rentalDetails: RentalDetailsInfo,
        deliveryInfo: DeliveryInfoData,
        paymentInfo: PaymentInfoData,
        transaction: TransactionInfo
      )

  type Model = AppState

  ghost predicate Inv(m: AppState) {
    m.rentalState == NotStarted || 
    m.rentalState == CartSelected || 
    m.rentalState == PeriodEntered || 
    m.rentalState == DeliveryInfoEntered || 
    m.rentalState == PaymentInfoEntered || 
    m.rentalState == TransactionComplete
  }

  function Init(): AppState {
    AppState(
      User("user1", "John Doe", true),
      Cart(map[]),
      NotStarted,
      RentalDetails(0, 0, map[]),
      DeliveryInfo("", ""),
      PaymentInfo(""),
      Transaction(map[], DeliveryInfo("", ""), PaymentInfo(""))
    )
  }

  function Apply(m: AppState, a: Action): AppState {
    match a
    case InitiateRent =>
      if m.user.isLoggedIn && |m.cart.items| > 0 then
        AppState(m.user, m.cart, CartSelected, m.rentalDetails, m.deliveryInfo, m.paymentInfo, m.transaction)
      else
        m
    case EnterRentalPeriod(period) =>
      if m.rentalState == CartSelected && period > 0 then
        AppState(m.user, m.cart, PeriodEntered, RentalDetails(period, 0, map[]), m.deliveryInfo, m.paymentInfo, m.transaction)
      else
        m
    case ConfirmRentalPeriod =>
      if m.rentalState == PeriodEntered then
        AppState(m.user, m.cart, DeliveryInfoEntered, RentalDetails(m.rentalDetails.period, 0, map[]), m.deliveryInfo, m.paymentInfo, m.transaction)
      else
        m
    case EnterDeliveryInfo(address, contact) =>
      if m.rentalState == DeliveryInfoEntered then
        AppState(m.user, m.cart, PaymentInfoEntered, m.rentalDetails, DeliveryInfo(address, contact), m.paymentInfo, m.transaction)
      else
        m
    case EnterPaymentInfo(payment) =>
      if m.rentalState == PaymentInfoEntered then
        AppState(m.user, m.cart, TransactionComplete, m.rentalDetails, m.deliveryInfo, PaymentInfo(payment), m.transaction)
      else
        m
    case CompleteTransaction =>
      if m.rentalState == TransactionComplete then
        AppState(m.user, m.cart, TransactionComplete, m.rentalDetails, m.deliveryInfo, m.paymentInfo, Transaction(m.cart.items, m.deliveryInfo, m.paymentInfo))
      else
        m
  }

  function Normalize(m: AppState): AppState {
    m
  }

  lemma InitSatisfiesInv()
    ensures Inv(Init())
  {
  }

  lemma StepPreservesInv(m: AppState, a: Action)
    ensures Inv(Normalize(Apply(m, a)))
  {
  }

  lemma RentInitiated(m: AppState)
    requires m.user.isLoggedIn && |m.cart.items| > 0
    ensures m.rentalState == NotStarted ==> Apply(m, InitiateRent).rentalState == CartSelected
  {
  }
}

module F4_6Kernel refines Kernel {
  import D = F4_6Domain
}