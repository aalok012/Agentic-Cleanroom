import sys
from typing import Callable, Any, TypeVar, NamedTuple
from math import floor
from itertools import count

import module_ as module_
import _dafny as _dafny
import System_ as System_

# Module: F3__2__REQ__6Domain

class default__:
    def  __init__(self):
        pass

    @staticmethod
    def Init():
        return _dafny.Map({})

    @staticmethod
    def Apply(m, a):
        source0_ = a
        if True:
            d_0_u_ = source0_.username
            d_1_p_ = source0_.password
            return (m).set(d_0_u_, d_1_p_)

    @staticmethod
    def Normalize(m):
        return m


class Action:
    @classmethod
    def default(cls, ):
        return lambda: Action_StoreCredential(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")))
    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)
    @property
    def is_StoreCredential(self) -> bool:
        return isinstance(self, Action_StoreCredential)

class Action_StoreCredential(Action, NamedTuple('StoreCredential', [('username', Any), ('password', Any)])):
    def __dafnystr__(self) -> str:
        return f'F3_2_REQ_6Domain.Action.StoreCredential({self.username.VerbatimString(True)}, {self.password.VerbatimString(True)})'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_StoreCredential) and self.username == __o.username and self.password == __o.password
    def __hash__(self) -> int:
        return super().__hash__()

