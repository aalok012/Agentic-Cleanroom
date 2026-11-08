import sys
from typing import Callable, Any, TypeVar, NamedTuple
from math import floor
from itertools import count

import module_ as module_
import _dafny as _dafny
import System_ as System_

# Module: F3__1__REQ__6Domain

class default__:
    def  __init__(self):
        pass

    @staticmethod
    def Init():
        return (_dafny.Map({}), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "size")))

    @staticmethod
    def Apply(m, a):
        let_tmp_rhs0_ = m
        d_0_torrents_ = let_tmp_rhs0_[0]
        d_1_sortCol_ = let_tmp_rhs0_[1]
        source0_ = a
        if True:
            if source0_.is_SortBySize:
                return (d_0_torrents_, _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "size")))
        if True:
            if source0_.is_SortByDate:
                return (d_0_torrents_, _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "date")))
        if True:
            return (d_0_torrents_, _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "alpha")))

    @staticmethod
    def Normalize(m):
        let_tmp_rhs0_ = m
        d_0_torrents_ = let_tmp_rhs0_[0]
        d_1_sortCol_ = let_tmp_rhs0_[1]
        if (((d_1_sortCol_) == (_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "size")))) or ((d_1_sortCol_) == (_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "date"))))) or ((d_1_sortCol_) == (_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "alpha")))):
            return m
        elif True:
            return (d_0_torrents_, _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "size")))


class Action:
    @_dafny.classproperty
    def AllSingletonConstructors(cls):
        return [Action_SortBySize(), Action_SortByDate(), Action_SortByAlpha()]
    @classmethod
    def default(cls, ):
        return lambda: Action_SortBySize()
    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)
    @property
    def is_SortBySize(self) -> bool:
        return isinstance(self, Action_SortBySize)
    @property
    def is_SortByDate(self) -> bool:
        return isinstance(self, Action_SortByDate)
    @property
    def is_SortByAlpha(self) -> bool:
        return isinstance(self, Action_SortByAlpha)

class Action_SortBySize(Action, NamedTuple('SortBySize', [])):
    def __dafnystr__(self) -> str:
        return f'F3_1_REQ_6Domain.Action.SortBySize'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_SortBySize)
    def __hash__(self) -> int:
        return super().__hash__()

class Action_SortByDate(Action, NamedTuple('SortByDate', [])):
    def __dafnystr__(self) -> str:
        return f'F3_1_REQ_6Domain.Action.SortByDate'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_SortByDate)
    def __hash__(self) -> int:
        return super().__hash__()

class Action_SortByAlpha(Action, NamedTuple('SortByAlpha', [])):
    def __dafnystr__(self) -> str:
        return f'F3_1_REQ_6Domain.Action.SortByAlpha'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_SortByAlpha)
    def __hash__(self) -> int:
        return super().__hash__()

