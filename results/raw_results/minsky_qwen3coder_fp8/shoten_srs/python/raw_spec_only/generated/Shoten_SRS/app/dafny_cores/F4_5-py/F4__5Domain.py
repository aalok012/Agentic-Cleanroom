import sys
from typing import Callable, Any, TypeVar, NamedTuple
from math import floor
from itertools import count

import module_ as module_
import _dafny as _dafny
import System_ as System_

# Module: F4__5Domain

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
            d_0_book_ = source0_
            if (d_0_book_) in (m):
                return (m) - (_dafny.Set({d_0_book_}))
            elif True:
                return m

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
    def is_Remove(self) -> bool:
        return isinstance(self, Action_Remove)

class Action_Remove(Action, NamedTuple('Remove', [('book', Any)])):
    def __dafnystr__(self) -> str:
        return f'F4_5Domain.Action.Remove({self.book.VerbatimString(True)})'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_Remove) and self.book == __o.book
    def __hash__(self) -> int:
        return super().__hash__()

