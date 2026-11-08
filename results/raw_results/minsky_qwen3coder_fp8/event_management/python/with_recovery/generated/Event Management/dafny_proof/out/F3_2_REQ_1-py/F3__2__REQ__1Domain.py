import sys
from typing import Callable, Any, TypeVar, NamedTuple
from math import floor
from itertools import count

import module_ as module_
import _dafny as _dafny
import System_ as System_

# Module: F3__2__REQ__1Domain

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
            return True

    @staticmethod
    def Normalize(m):
        return m


class Action:
    @_dafny.classproperty
    def AllSingletonConstructors(cls):
        return [Action_Access()]
    @classmethod
    def default(cls, ):
        return lambda: Action_Access()
    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)
    @property
    def is_Access(self) -> bool:
        return isinstance(self, Action_Access)

class Action_Access(Action, NamedTuple('Access', [])):
    def __dafnystr__(self) -> str:
        return f'F3_2_REQ_1Domain.Action.Access'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_Access)
    def __hash__(self) -> int:
        return super().__hash__()

