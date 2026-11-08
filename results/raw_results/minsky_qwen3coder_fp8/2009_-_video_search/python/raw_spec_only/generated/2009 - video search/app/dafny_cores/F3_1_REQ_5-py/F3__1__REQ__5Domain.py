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
        return (_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")), _dafny.Map({}))

    @staticmethod
    def Apply(m, a):
        source0_ = a
        if True:
            d_0_query_ = source0_
            if (d_0_query_) == (_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, ""))):
                return (_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "No results were found for this search.")), _dafny.Map({}))
            elif True:
                return (d_0_query_, _dafny.Map({}))

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
    def is_Search(self) -> bool:
        return isinstance(self, Action_Search)

class Action_Search(Action, NamedTuple('Search', [('query', Any)])):
    def __dafnystr__(self) -> str:
        return f'F3_1_REQ_5Domain.Action.Search({self.query.VerbatimString(True)})'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_Search) and self.query == __o.query
    def __hash__(self) -> int:
        return super().__hash__()

