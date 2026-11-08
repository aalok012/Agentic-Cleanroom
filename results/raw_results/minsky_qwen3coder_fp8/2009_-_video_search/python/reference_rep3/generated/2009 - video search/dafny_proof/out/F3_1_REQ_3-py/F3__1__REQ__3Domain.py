import sys
from typing import Callable, Any, TypeVar, NamedTuple
from math import floor
from itertools import count

import module_ as module_
import _dafny as _dafny
import System_ as System_

# Module: F3__1__REQ__3Domain

class default__:
    def  __init__(self):
        pass

    @staticmethod
    def Init():
        return False

    @staticmethod
    def Apply(m, a):
        source0_ = a
        if True:
            return not(m)

    @staticmethod
    def Normalize(m):
        return m


class Action:
    @_dafny.classproperty
    def AllSingletonConstructors(cls):
        return [Action_ToggleSearch()]
    @classmethod
    def default(cls, ):
        return lambda: Action_ToggleSearch()
    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)
    @property
    def is_ToggleSearch(self) -> bool:
        return isinstance(self, Action_ToggleSearch)

class Action_ToggleSearch(Action, NamedTuple('ToggleSearch', [])):
    def __dafnystr__(self) -> str:
        return f'F3_1_REQ_3Domain.Action.ToggleSearch'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_ToggleSearch)
    def __hash__(self) -> int:
        return super().__hash__()

