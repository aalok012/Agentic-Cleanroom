import sys
from typing import Callable, Any, TypeVar, NamedTuple
from math import floor
from itertools import count

import module_ as module_
import _dafny as _dafny
import System_ as System_

# Module: F4__13Domain

class default__:
    def  __init__(self):
        pass

    @staticmethod
    def Init():
        return (_dafny.Map({}), _dafny.Map({}))

    @staticmethod
    def Apply(m, a):
        source0_ = a
        if True:
            if source0_.is_ViewPurchaseHistory:
                return m
        if True:
            d_0_orderId_ = source0_.orderId
            return m

    @staticmethod
    def Normalize(m):
        return m


class Purchase:
    @classmethod
    def default(cls, ):
        return lambda: Purchase_Purchase(int(0), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")))
    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)
    @property
    def is_Purchase(self) -> bool:
        return isinstance(self, Purchase_Purchase)

class Purchase_Purchase(Purchase, NamedTuple('Purchase', [('date', Any), ('paymentMode', Any)])):
    def __dafnystr__(self) -> str:
        return f'F4_13Domain.Purchase.Purchase({_dafny.string_of(self.date)}, {self.paymentMode.VerbatimString(True)})'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Purchase_Purchase) and self.date == __o.date and self.paymentMode == __o.paymentMode
    def __hash__(self) -> int:
        return super().__hash__()


class Order:
    @classmethod
    def default(cls, ):
        return lambda: _dafny.Map({})
    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)
    @property
    def is_Order(self) -> bool:
        return isinstance(self, Order_Order)

class Order_Order(Order, NamedTuple('Order', [('items', Any)])):
    def __dafnystr__(self) -> str:
        return f'F4_13Domain.Order.Order({_dafny.string_of(self.items)})'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Order_Order) and self.items == __o.items
    def __hash__(self) -> int:
        return super().__hash__()


class Action:
    @classmethod
    def default(cls, ):
        return lambda: Action_ViewPurchaseHistory()
    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)
    @property
    def is_ViewPurchaseHistory(self) -> bool:
        return isinstance(self, Action_ViewPurchaseHistory)
    @property
    def is_ViewOrderDetails(self) -> bool:
        return isinstance(self, Action_ViewOrderDetails)

class Action_ViewPurchaseHistory(Action, NamedTuple('ViewPurchaseHistory', [])):
    def __dafnystr__(self) -> str:
        return f'F4_13Domain.Action.ViewPurchaseHistory'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_ViewPurchaseHistory)
    def __hash__(self) -> int:
        return super().__hash__()

class Action_ViewOrderDetails(Action, NamedTuple('ViewOrderDetails', [('orderId', Any)])):
    def __dafnystr__(self) -> str:
        return f'F4_13Domain.Action.ViewOrderDetails({_dafny.string_of(self.orderId)})'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_ViewOrderDetails) and self.orderId == __o.orderId
    def __hash__(self) -> int:
        return super().__hash__()

