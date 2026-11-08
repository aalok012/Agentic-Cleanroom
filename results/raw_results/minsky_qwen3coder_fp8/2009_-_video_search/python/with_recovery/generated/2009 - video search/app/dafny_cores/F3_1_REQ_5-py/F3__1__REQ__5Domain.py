import sys
from typing import Callable, Any, TypeVar, NamedTuple
from math import floor
from itertools import count

import module_ as module_
import _dafny as _dafny
import System_ as System_

# Module: F3__1__REQ__5Domain

class default__:
    def  __init__(self):
        pass

    @staticmethod
    def Init():
        return _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, ""))

    @staticmethod
    def Apply(m, a):
        source0_ = a
        if True:
            return _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "No results were found for this search."))

    @staticmethod
    def Normalize(m):
        return m


class Action:
    @_dafny.classproperty
    def AllSingletonConstructors(cls):
        return [Action_SearchNoResults()]
    @classmethod
    def default(cls, ):
        return lambda: Action_SearchNoResults()
    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)
    @property
    def is_SearchNoResults(self) -> bool:
        return isinstance(self, Action_SearchNoResults)

class Action_SearchNoResults(Action, NamedTuple('SearchNoResults', [])):
    def __dafnystr__(self) -> str:
        return f'F3_1_REQ_5Domain.Action.SearchNoResults'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_SearchNoResults)
    def __hash__(self) -> int:
        return super().__hash__()

