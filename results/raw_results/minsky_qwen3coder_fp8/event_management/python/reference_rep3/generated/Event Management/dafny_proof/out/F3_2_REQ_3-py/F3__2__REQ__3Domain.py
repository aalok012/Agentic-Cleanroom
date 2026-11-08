import sys
from typing import Callable, Any, TypeVar, NamedTuple
from math import floor
from itertools import count

import module_ as module_
import _dafny as _dafny
import System_ as System_

# Module: F3__2__REQ__3Domain

class default__:
    def  __init__(self):
        pass

    @staticmethod
    def Init():
        return (_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")), _dafny.Map({}))

    @staticmethod
    def Apply(m, a):
        source0_ = a
        if True:
            let_tmp_rhs0_ = m
            d_0___v1_ = let_tmp_rhs0_[0]
            d_1_errors_ = let_tmp_rhs0_[1]
            return (_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "Invalid input provided by user")), d_1_errors_)

    @staticmethod
    def Normalize(m):
        let_tmp_rhs0_ = m
        d_0_msg_ = let_tmp_rhs0_[0]
        d_1_errors_ = let_tmp_rhs0_[1]
        if (d_0_msg_) == (_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, ""))):
            return (d_0_msg_, d_1_errors_)
        elif True:
            return (d_0_msg_, d_1_errors_)


class Action:
    @_dafny.classproperty
    def AllSingletonConstructors(cls):
        return [Action_Error()]
    @classmethod
    def default(cls, ):
        return lambda: Action_Error()
    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)
    @property
    def is_Error(self) -> bool:
        return isinstance(self, Action_Error)

class Action_Error(Action, NamedTuple('Error', [])):
    def __dafnystr__(self) -> str:
        return f'F3_2_REQ_3Domain.Action.Error'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_Error)
    def __hash__(self) -> int:
        return super().__hash__()

