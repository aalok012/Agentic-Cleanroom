import sys
from typing import Callable, Any, TypeVar, NamedTuple
from math import floor
from itertools import count

import module_ as module_
import _dafny as _dafny
import System_ as System_

# Module: F4__6Domain

class default__:
    def  __init__(self):
        pass

    @staticmethod
    def Init():
        return (_dafny.Map({}), _dafny.Map({}), _dafny.Map({}), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")))

    @staticmethod
    def Apply(m, a):
        let_tmp_rhs0_ = m
        d_0_cart_ = let_tmp_rhs0_[0]
        d_1_rentCharges_ = let_tmp_rhs0_[1]
        d_2_bookPrices_ = let_tmp_rhs0_[2]
        d_3_period_ = let_tmp_rhs0_[3]
        d_4_deliveryInfo_ = let_tmp_rhs0_[4]
        d_5_paymentInfo_ = let_tmp_rhs0_[5]
        d_6_transactionStatus_ = let_tmp_rhs0_[6]
        source0_ = a
        if True:
            if source0_.is_RentBooks:
                return (d_0_cart_, d_1_rentCharges_, d_2_bookPrices_, d_3_period_, d_4_deliveryInfo_, d_5_paymentInfo_, _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "renting")))
        if True:
            if source0_.is_EnterRentalPeriod:
                d_7_p_ = source0_.period
                return (d_0_cart_, d_1_rentCharges_, d_2_bookPrices_, d_7_p_, d_4_deliveryInfo_, d_5_paymentInfo_, d_6_transactionStatus_)
        if True:
            if source0_.is_DisplayRentCharges:
                return (d_0_cart_, d_1_rentCharges_, d_2_bookPrices_, d_3_period_, d_4_deliveryInfo_, d_5_paymentInfo_, d_6_transactionStatus_)
        if True:
            if source0_.is_EnterDeliveryInfo:
                d_8_d_ = source0_.deliveryInfo
                return (d_0_cart_, d_1_rentCharges_, d_2_bookPrices_, d_3_period_, d_8_d_, d_5_paymentInfo_, d_6_transactionStatus_)
        if True:
            if source0_.is_EnterPaymentInfo:
                d_9_p_ = source0_.paymentInfo
                return (d_0_cart_, d_1_rentCharges_, d_2_bookPrices_, d_3_period_, d_4_deliveryInfo_, d_9_p_, d_6_transactionStatus_)
        if True:
            return (_dafny.Map({}), _dafny.Map({}), _dafny.Map({}), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "completed")))

    @staticmethod
    def Normalize(m):
        let_tmp_rhs0_ = m
        d_0_cart_ = let_tmp_rhs0_[0]
        d_1_rentCharges_ = let_tmp_rhs0_[1]
        d_2_bookPrices_ = let_tmp_rhs0_[2]
        d_3_period_ = let_tmp_rhs0_[3]
        d_4_deliveryInfo_ = let_tmp_rhs0_[4]
        d_5_paymentInfo_ = let_tmp_rhs0_[5]
        d_6_transactionStatus_ = let_tmp_rhs0_[6]
        if (((((d_0_cart_) == (_dafny.Map({}))) and ((d_3_period_) == (_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, ""))))) and ((d_4_deliveryInfo_) == (_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, ""))))) and ((d_5_paymentInfo_) == (_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, ""))))) and ((d_6_transactionStatus_) == (_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "completed")))):
            return (_dafny.Map({}), _dafny.Map({}), _dafny.Map({}), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")))
        elif True:
            return m


class Action:
    @classmethod
    def default(cls, ):
        return lambda: Action_RentBooks()
    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)
    @property
    def is_RentBooks(self) -> bool:
        return isinstance(self, Action_RentBooks)
    @property
    def is_EnterRentalPeriod(self) -> bool:
        return isinstance(self, Action_EnterRentalPeriod)
    @property
    def is_DisplayRentCharges(self) -> bool:
        return isinstance(self, Action_DisplayRentCharges)
    @property
    def is_EnterDeliveryInfo(self) -> bool:
        return isinstance(self, Action_EnterDeliveryInfo)
    @property
    def is_EnterPaymentInfo(self) -> bool:
        return isinstance(self, Action_EnterPaymentInfo)
    @property
    def is_ConfirmTransaction(self) -> bool:
        return isinstance(self, Action_ConfirmTransaction)

class Action_RentBooks(Action, NamedTuple('RentBooks', [])):
    def __dafnystr__(self) -> str:
        return f'F4_6Domain.Action.RentBooks'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_RentBooks)
    def __hash__(self) -> int:
        return super().__hash__()

class Action_EnterRentalPeriod(Action, NamedTuple('EnterRentalPeriod', [('period', Any)])):
    def __dafnystr__(self) -> str:
        return f'F4_6Domain.Action.EnterRentalPeriod({self.period.VerbatimString(True)})'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_EnterRentalPeriod) and self.period == __o.period
    def __hash__(self) -> int:
        return super().__hash__()

class Action_DisplayRentCharges(Action, NamedTuple('DisplayRentCharges', [])):
    def __dafnystr__(self) -> str:
        return f'F4_6Domain.Action.DisplayRentCharges'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_DisplayRentCharges)
    def __hash__(self) -> int:
        return super().__hash__()

class Action_EnterDeliveryInfo(Action, NamedTuple('EnterDeliveryInfo', [('deliveryInfo', Any)])):
    def __dafnystr__(self) -> str:
        return f'F4_6Domain.Action.EnterDeliveryInfo({self.deliveryInfo.VerbatimString(True)})'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_EnterDeliveryInfo) and self.deliveryInfo == __o.deliveryInfo
    def __hash__(self) -> int:
        return super().__hash__()

class Action_EnterPaymentInfo(Action, NamedTuple('EnterPaymentInfo', [('paymentInfo', Any)])):
    def __dafnystr__(self) -> str:
        return f'F4_6Domain.Action.EnterPaymentInfo({self.paymentInfo.VerbatimString(True)})'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_EnterPaymentInfo) and self.paymentInfo == __o.paymentInfo
    def __hash__(self) -> int:
        return super().__hash__()

class Action_ConfirmTransaction(Action, NamedTuple('ConfirmTransaction', [])):
    def __dafnystr__(self) -> str:
        return f'F4_6Domain.Action.ConfirmTransaction'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_ConfirmTransaction)
    def __hash__(self) -> int:
        return super().__hash__()

