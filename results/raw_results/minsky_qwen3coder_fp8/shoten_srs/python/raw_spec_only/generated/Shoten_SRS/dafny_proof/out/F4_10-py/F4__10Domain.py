import sys
from typing import Callable, Any, TypeVar, NamedTuple
from math import floor
from itertools import count

import module_ as module_
import _dafny as _dafny
import System_ as System_

# Module: F4__10Domain

class default__:
    def  __init__(self):
        pass

    @staticmethod
    def Init():
        return (_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "Bookstore Address")), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "Bookstore Phone")), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "Bookstore Email")), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "Printstore Address")), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "Printstore Phone")), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "Printstore Email")), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "Student Address")), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "Student Phone")), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "Student Email")), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "Bookstore Directions")), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "Printstore Directions")), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "Student Directions")))

    @staticmethod
    def Apply(m, a):
        source0_ = a
        if True:
            if source0_.is_ViewContactInfo:
                let_tmp_rhs0_ = m
                d_0_bookstoreAddr_ = let_tmp_rhs0_[0]
                d_1_bookstorePhone_ = let_tmp_rhs0_[1]
                d_2_bookstoreEmail_ = let_tmp_rhs0_[2]
                d_3_printstoreAddr_ = let_tmp_rhs0_[3]
                d_4_printstorePhone_ = let_tmp_rhs0_[4]
                d_5_printstoreEmail_ = let_tmp_rhs0_[5]
                d_6_studentAddr_ = let_tmp_rhs0_[6]
                d_7_studentPhone_ = let_tmp_rhs0_[7]
                d_8_studentEmail_ = let_tmp_rhs0_[8]
                d_9_bookstoreDir_ = let_tmp_rhs0_[9]
                d_10_printstoreDir_ = let_tmp_rhs0_[10]
                d_11_studentDir_ = let_tmp_rhs0_[11]
                return (d_0_bookstoreAddr_, d_1_bookstorePhone_, d_2_bookstoreEmail_, d_3_printstoreAddr_, d_4_printstorePhone_, d_5_printstoreEmail_, d_6_studentAddr_, d_7_studentPhone_, d_8_studentEmail_, d_9_bookstoreDir_, d_10_printstoreDir_, d_11_studentDir_)
        if True:
            if source0_.is_DisplayStoreDetails:
                let_tmp_rhs1_ = m
                d_12_bookstoreAddr_ = let_tmp_rhs1_[0]
                d_13_bookstorePhone_ = let_tmp_rhs1_[1]
                d_14_bookstoreEmail_ = let_tmp_rhs1_[2]
                d_15_printstoreAddr_ = let_tmp_rhs1_[3]
                d_16_printstorePhone_ = let_tmp_rhs1_[4]
                d_17_printstoreEmail_ = let_tmp_rhs1_[5]
                d_18_studentAddr_ = let_tmp_rhs1_[6]
                d_19_studentPhone_ = let_tmp_rhs1_[7]
                d_20_studentEmail_ = let_tmp_rhs1_[8]
                d_21_bookstoreDir_ = let_tmp_rhs1_[9]
                d_22_printstoreDir_ = let_tmp_rhs1_[10]
                d_23_studentDir_ = let_tmp_rhs1_[11]
                return (d_12_bookstoreAddr_, d_13_bookstorePhone_, d_14_bookstoreEmail_, d_15_printstoreAddr_, d_16_printstorePhone_, d_17_printstoreEmail_, d_18_studentAddr_, d_19_studentPhone_, d_20_studentEmail_, d_21_bookstoreDir_, d_22_printstoreDir_, d_23_studentDir_)
        if True:
            let_tmp_rhs2_ = m
            d_24_bookstoreAddr_ = let_tmp_rhs2_[0]
            d_25_bookstorePhone_ = let_tmp_rhs2_[1]
            d_26_bookstoreEmail_ = let_tmp_rhs2_[2]
            d_27_printstoreAddr_ = let_tmp_rhs2_[3]
            d_28_printstorePhone_ = let_tmp_rhs2_[4]
            d_29_printstoreEmail_ = let_tmp_rhs2_[5]
            d_30_studentAddr_ = let_tmp_rhs2_[6]
            d_31_studentPhone_ = let_tmp_rhs2_[7]
            d_32_studentEmail_ = let_tmp_rhs2_[8]
            d_33_bookstoreDir_ = let_tmp_rhs2_[9]
            d_34_printstoreDir_ = let_tmp_rhs2_[10]
            d_35_studentDir_ = let_tmp_rhs2_[11]
            return (d_24_bookstoreAddr_, d_25_bookstorePhone_, d_26_bookstoreEmail_, d_27_printstoreAddr_, d_28_printstorePhone_, d_29_printstoreEmail_, d_30_studentAddr_, d_31_studentPhone_, d_32_studentEmail_, d_33_bookstoreDir_, d_34_printstoreDir_, d_35_studentDir_)

    @staticmethod
    def Normalize(m):
        return m


class Action:
    @_dafny.classproperty
    def AllSingletonConstructors(cls):
        return [Action_ViewContactInfo(), Action_DisplayStoreDetails(), Action_ShowMap()]
    @classmethod
    def default(cls, ):
        return lambda: Action_ViewContactInfo()
    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)
    @property
    def is_ViewContactInfo(self) -> bool:
        return isinstance(self, Action_ViewContactInfo)
    @property
    def is_DisplayStoreDetails(self) -> bool:
        return isinstance(self, Action_DisplayStoreDetails)
    @property
    def is_ShowMap(self) -> bool:
        return isinstance(self, Action_ShowMap)

class Action_ViewContactInfo(Action, NamedTuple('ViewContactInfo', [])):
    def __dafnystr__(self) -> str:
        return f'F4_10Domain.Action.ViewContactInfo'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_ViewContactInfo)
    def __hash__(self) -> int:
        return super().__hash__()

class Action_DisplayStoreDetails(Action, NamedTuple('DisplayStoreDetails', [])):
    def __dafnystr__(self) -> str:
        return f'F4_10Domain.Action.DisplayStoreDetails'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_DisplayStoreDetails)
    def __hash__(self) -> int:
        return super().__hash__()

class Action_ShowMap(Action, NamedTuple('ShowMap', [])):
    def __dafnystr__(self) -> str:
        return f'F4_10Domain.Action.ShowMap'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_ShowMap)
    def __hash__(self) -> int:
        return super().__hash__()

