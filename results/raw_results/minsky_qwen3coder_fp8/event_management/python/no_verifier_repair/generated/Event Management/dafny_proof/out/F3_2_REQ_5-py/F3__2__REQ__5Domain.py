import sys
from typing import Callable, Any, TypeVar, NamedTuple
from math import floor
from itertools import count

import module_ as module_
import _dafny as _dafny
import System_ as System_

# Module: F3__2__REQ__5Domain

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
            return m

    @staticmethod
    def Normalize(m):
        return m


class Action:
    @_dafny.classproperty
    def AllSingletonConstructors(cls):
        return [Action_GetRegistrants()]
    @classmethod
    def default(cls, ):
        return lambda: Action_GetRegistrants()
    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)
    @property
    def is_GetRegistrants(self) -> bool:
        return isinstance(self, Action_GetRegistrants)

class Action_GetRegistrants(Action, NamedTuple('GetRegistrants', [])):
    def __dafnystr__(self) -> str:
        return f'F3_2_REQ_5Domain.Action.GetRegistrants'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_GetRegistrants)
    def __hash__(self) -> int:
        return super().__hash__()

