import sys
from typing import Callable, Any, TypeVar, NamedTuple
from math import floor
from itertools import count

import module_ as module_
import _dafny as _dafny
import System_ as System_
import F3__2__REQ__3Domain as F3__2__REQ__3Domain

# Module: F3__2__REQ__3Kernel

class default__:
    def  __init__(self):
        pass

    @staticmethod
    def Step(m, a):
        return F3__2__REQ__3Domain.default__.Normalize(F3__2__REQ__3Domain.default__.Apply(m, a))

    @staticmethod
    def InitHistory():
        return History_History(_dafny.SeqWithoutIsStrInference([]), F3__2__REQ__3Domain.default__.Init(), _dafny.SeqWithoutIsStrInference([]))

    @staticmethod
    def Do(h, a):
        return History_History(((h).past) + (_dafny.SeqWithoutIsStrInference([(h).present])), default__.Step((h).present, a), _dafny.SeqWithoutIsStrInference([]))

    @staticmethod
    def Preview(h, a):
        return History_History((h).past, default__.Step((h).present, a), (h).future)

    @staticmethod
    def CommitFrom(h, baseline):
        return History_History(((h).past) + (_dafny.SeqWithoutIsStrInference([baseline])), (h).present, _dafny.SeqWithoutIsStrInference([]))

    @staticmethod
    def Undo(h):
        if (len((h).past)) == (0):
            return h
        elif True:
            d_0_i_ = (len((h).past)) - (1)
            return History_History(_dafny.SeqWithoutIsStrInference(((h).past)[:d_0_i_:]), ((h).past)[d_0_i_], (_dafny.SeqWithoutIsStrInference([(h).present])) + ((h).future))

    @staticmethod
    def Redo(h):
        if (len((h).future)) == (0):
            return h
        elif True:
            return History_History(((h).past) + (_dafny.SeqWithoutIsStrInference([(h).present])), ((h).future)[0], _dafny.SeqWithoutIsStrInference(((h).future)[1::]))


class History:
    @classmethod
    def default(cls, ):
        return lambda: History_History(_dafny.Seq({}), (_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")), False), _dafny.Seq({}))
    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)
    @property
    def is_History(self) -> bool:
        return isinstance(self, History_History)

class History_History(History, NamedTuple('History', [('past', Any), ('present', Any), ('future', Any)])):
    def __dafnystr__(self) -> str:
        return f'F3_2_REQ_3Kernel.History.History({_dafny.string_of(self.past)}, {_dafny.string_of(self.present)}, {_dafny.string_of(self.future)})'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, History_History) and self.past == __o.past and self.present == __o.present and self.future == __o.future
    def __hash__(self) -> int:
        return super().__hash__()

