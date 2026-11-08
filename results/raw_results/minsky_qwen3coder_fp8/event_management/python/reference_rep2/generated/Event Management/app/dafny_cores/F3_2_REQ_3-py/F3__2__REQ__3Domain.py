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
        return (_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")), False)

    @staticmethod
    def Apply(m, a):
        source0_ = a
        if True:
            return (_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "Invalid input provided by user")), True)

    @staticmethod
    def Normalize(m):
        return m


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

