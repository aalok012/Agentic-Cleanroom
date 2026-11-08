import sys
from typing import Callable, Any, TypeVar, NamedTuple
from math import floor
from itertools import count

import module_ as module_
import _dafny as _dafny
import System_ as System_

# Module: F3__2__REQ__10Domain

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
            d_0_id_ = source0_.eventId
            d_1_data_ = source0_.eventData
            return (m).set(d_0_id_, d_1_data_)

    @staticmethod
    def Normalize(m):
        return m


class Action:
    @classmethod
    def default(cls, ):
        return lambda: Action_AppendEvent(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")))
    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)
    @property
    def is_AppendEvent(self) -> bool:
        return isinstance(self, Action_AppendEvent)

class Action_AppendEvent(Action, NamedTuple('AppendEvent', [('eventId', Any), ('eventData', Any)])):
    def __dafnystr__(self) -> str:
        return f'F3_2_REQ_10Domain.Action.AppendEvent({self.eventId.VerbatimString(True)}, {self.eventData.VerbatimString(True)})'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_AppendEvent) and self.eventId == __o.eventId and self.eventData == __o.eventData
    def __hash__(self) -> int:
        return super().__hash__()

