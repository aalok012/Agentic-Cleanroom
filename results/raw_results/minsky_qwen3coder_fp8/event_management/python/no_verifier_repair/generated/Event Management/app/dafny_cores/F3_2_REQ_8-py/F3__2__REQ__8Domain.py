import sys
from typing import Callable, Any, TypeVar, NamedTuple
from math import floor
from itertools import count

import module_ as module_
import _dafny as _dafny
import System_ as System_

# Module: F3__2__REQ__8Domain

class default__:
    def  __init__(self):
        pass

    @staticmethod
    def Init():
        return (_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "user")), False)

    @staticmethod
    def Apply(m, a):
        source0_ = a
        if True:
            d_0_adminId_ = source0_.adminId
            d_1_clientId_ = source0_.clientId
            if ((m)[0]) == (_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "admin"))):
                return ((m)[0], True)
            elif True:
                return m

    @staticmethod
    def Normalize(m):
        if ((m)[0]) == (_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "admin"))):
            return m
        elif True:
            return (_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "user")), False)


class Action:
    @classmethod
    def default(cls, ):
        return lambda: Action_AccessClientData(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")))
    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)
    @property
    def is_AccessClientData(self) -> bool:
        return isinstance(self, Action_AccessClientData)

class Action_AccessClientData(Action, NamedTuple('AccessClientData', [('adminId', Any), ('clientId', Any)])):
    def __dafnystr__(self) -> str:
        return f'F3_2_REQ_8Domain.Action.AccessClientData({self.adminId.VerbatimString(True)}, {self.clientId.VerbatimString(True)})'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_AccessClientData) and self.adminId == __o.adminId and self.clientId == __o.clientId
    def __hash__(self) -> int:
        return super().__hash__()

