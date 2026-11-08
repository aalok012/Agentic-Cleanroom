import sys
from typing import Callable, Any, TypeVar, NamedTuple
from math import floor
from itertools import count

import module_ as module_
import _dafny as _dafny
import System_ as System_

# Module: F4__14Domain

class default__:
    def  __init__(self):
        pass

    @staticmethod
    def Init():
        return (False, _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")))

    @staticmethod
    def Apply(m, a):
        source0_ = a
        if True:
            return (False, _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")))

    @staticmethod
    def Normalize(m):
        return m


class Action:
    @_dafny.classproperty
    def AllSingletonConstructors(cls):
        return [Action_Logout()]
    @classmethod
    def default(cls, ):
        return lambda: Action_Logout()
    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)
    @property
    def is_Logout(self) -> bool:
        return isinstance(self, Action_Logout)

class Action_Logout(Action, NamedTuple('Logout', [])):
    def __dafnystr__(self) -> str:
        return f'F4_14Domain.Action.Logout'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_Logout)
    def __hash__(self) -> int:
        return super().__hash__()

