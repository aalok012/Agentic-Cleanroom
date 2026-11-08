import sys
from typing import Callable, Any, TypeVar, NamedTuple
from math import floor
from itertools import count

import module_ as module_
import _dafny as _dafny
import System_ as System_

# Module: F3__1__REQ__2Domain

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
        return [Action_UpdateSites()]
    @classmethod
    def default(cls, ):
        return lambda: Action_UpdateSites()
    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)
    @property
    def is_UpdateSites(self) -> bool:
        return isinstance(self, Action_UpdateSites)

class Action_UpdateSites(Action, NamedTuple('UpdateSites', [])):
    def __dafnystr__(self) -> str:
        return f'F3_1_REQ_2Domain.Action.UpdateSites'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_UpdateSites)
    def __hash__(self) -> int:
        return super().__hash__()

