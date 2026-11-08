import sys
from typing import Callable, Any, TypeVar, NamedTuple
from math import floor
from itertools import count

import module_ as module_
import _dafny as _dafny
import System_ as System_

# Module: F3__2__REQ__9Domain

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
            d_0_clientId_ = source0_.clientId
            d_1_permissions_ = source0_.permissions
            if (d_0_clientId_) in (m):
                return (m).set(d_0_clientId_, ((m)[d_0_clientId_]) | (d_1_permissions_))
            elif True:
                return (m).set(d_0_clientId_, d_1_permissions_)

    @staticmethod
    def Normalize(m):
        return m


class Action:
    @classmethod
    def default(cls, ):
        return lambda: Action_AddClientAccess(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")), _dafny.Set({}))
    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)
    @property
    def is_AddClientAccess(self) -> bool:
        return isinstance(self, Action_AddClientAccess)

class Action_AddClientAccess(Action, NamedTuple('AddClientAccess', [('clientId', Any), ('permissions', Any)])):
    def __dafnystr__(self) -> str:
        return f'F3_2_REQ_9Domain.Action.AddClientAccess({self.clientId.VerbatimString(True)}, {_dafny.string_of(self.permissions)})'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_AddClientAccess) and self.clientId == __o.clientId and self.permissions == __o.permissions
    def __hash__(self) -> int:
        return super().__hash__()

