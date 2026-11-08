import sys
from typing import Callable, Any, TypeVar, NamedTuple
from math import floor
from itertools import count

import module_ as module_
import _dafny as _dafny
import System_ as System_

# Module: F3__1__REQ__1Domain

class default__:
    def  __init__(self):
        pass

    @staticmethod
    def Init():
        return (_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")), _dafny.Set({}), _dafny.Set({}))

    @staticmethod
    def Apply(m, a):
        source0_ = a
        if True:
            d_0_q_ = source0_
            let_tmp_rhs0_ = m
            d_1_old__q_ = let_tmp_rhs0_[0]
            d_2_torrents_ = let_tmp_rhs0_[1]
            d_3_streams_ = let_tmp_rhs0_[2]
            return (d_0_q_, d_2_torrents_, d_3_streams_)

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
        return f'F3_1_REQ_1Domain.Action.Search({self.query.VerbatimString(True)})'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_Search) and self.query == __o.query
    def __hash__(self) -> int:
        return super().__hash__()

