import sys
from typing import Callable, Any, TypeVar, NamedTuple
from math import floor
from itertools import count

import module_ as module_
import _dafny as _dafny
import System_ as System_

# Module: F4__11Domain

class default__:
    def  __init__(self):
        pass

    @staticmethod
    def Init():
        return (_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")))

    @staticmethod
    def Apply(m, a):
        source0_ = a
        if True:
            if source0_.is_UpdateAccountInfo:
                d_0_name_ = source0_.name
                d_1_mailingAddr_ = source0_.mailingAddr
                d_2_billingAddr_ = source0_.billingAddr
                d_3_paymentInfo_ = source0_.paymentInfo
                let_tmp_rhs0_ = m
                d_4_oldName_ = let_tmp_rhs0_[0]
                d_5_oldMailAddr_ = let_tmp_rhs0_[1]
                d_6_oldBillAddr_ = let_tmp_rhs0_[2]
                d_7_oldPayInfo_ = let_tmp_rhs0_[3]
                d_8_oldPass_ = let_tmp_rhs0_[4]
                d_9_newPass_ = let_tmp_rhs0_[5]
                return (d_0_name_, d_1_mailingAddr_, d_2_billingAddr_, d_3_paymentInfo_, d_8_oldPass_, d_9_newPass_)
        if True:
            d_10_oldPass_ = source0_.oldPass
            d_11_newPass1_ = source0_.newPass1
            d_12_newPass2_ = source0_.newPass2
            let_tmp_rhs1_ = m
            d_13_name_ = let_tmp_rhs1_[0]
            d_14_mailAddr_ = let_tmp_rhs1_[1]
            d_15_billAddr_ = let_tmp_rhs1_[2]
            d_16_payInfo_ = let_tmp_rhs1_[3]
            d_17_oldPassStored_ = let_tmp_rhs1_[4]
            d_18_newPassStored_ = let_tmp_rhs1_[5]
            if ((d_10_oldPass_) == (d_17_oldPassStored_)) and ((d_11_newPass1_) == (d_12_newPass2_)):
                return (d_13_name_, d_14_mailAddr_, d_15_billAddr_, d_16_payInfo_, d_10_oldPass_, d_11_newPass1_)
            elif True:
                return m

    @staticmethod
    def Normalize(m):
        return m


class Action:
    @classmethod
    def default(cls, ):
        return lambda: Action_UpdateAccountInfo(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")))
    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)
    @property
    def is_UpdateAccountInfo(self) -> bool:
        return isinstance(self, Action_UpdateAccountInfo)
    @property
    def is_ChangePassword(self) -> bool:
        return isinstance(self, Action_ChangePassword)

class Action_UpdateAccountInfo(Action, NamedTuple('UpdateAccountInfo', [('name', Any), ('mailingAddr', Any), ('billingAddr', Any), ('paymentInfo', Any)])):
    def __dafnystr__(self) -> str:
        return f'F4_11Domain.Action.UpdateAccountInfo({self.name.VerbatimString(True)}, {self.mailingAddr.VerbatimString(True)}, {self.billingAddr.VerbatimString(True)}, {self.paymentInfo.VerbatimString(True)})'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_UpdateAccountInfo) and self.name == __o.name and self.mailingAddr == __o.mailingAddr and self.billingAddr == __o.billingAddr and self.paymentInfo == __o.paymentInfo
    def __hash__(self) -> int:
        return super().__hash__()

class Action_ChangePassword(Action, NamedTuple('ChangePassword', [('oldPass', Any), ('newPass1', Any), ('newPass2', Any)])):
    def __dafnystr__(self) -> str:
        return f'F4_11Domain.Action.ChangePassword({self.oldPass.VerbatimString(True)}, {self.newPass1.VerbatimString(True)}, {self.newPass2.VerbatimString(True)})'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_ChangePassword) and self.oldPass == __o.oldPass and self.newPass1 == __o.newPass1 and self.newPass2 == __o.newPass2
    def __hash__(self) -> int:
        return super().__hash__()

