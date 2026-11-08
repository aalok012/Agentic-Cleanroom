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
        return _dafny.Map({})

    @staticmethod
    def Apply(m, a):
        source0_ = a
        if True:
            d_0_clientId_ = source0_
            return (m).set(d_0_clientId_, True)

    @staticmethod
    def Normalize(m):
        return m


class Action:
    @classmethod
    def default(cls, ):
        return lambda: _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, ""))
    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)
    @property
    def is_GrantAccess(self) -> bool:
        return isinstance(self, Action_GrantAccess)

class Action_GrantAccess(Action, NamedTuple('GrantAccess', [('clientId', Any)])):
    def __dafnystr__(self) -> str:
        return f'F3_2_REQ_8Domain.Action.GrantAccess({self.clientId.VerbatimString(True)})'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_GrantAccess) and self.clientId == __o.clientId
    def __hash__(self) -> int:
        return super().__hash__()

