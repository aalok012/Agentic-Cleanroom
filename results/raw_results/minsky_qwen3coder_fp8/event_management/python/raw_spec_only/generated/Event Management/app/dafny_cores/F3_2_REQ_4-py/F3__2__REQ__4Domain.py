import sys
from typing import Callable, Any, TypeVar, NamedTuple
from math import floor
from itertools import count

import module_ as module_
import _dafny as _dafny
import System_ as System_

# Module: F3__2__REQ__4Domain

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
            d_0_eventId_ = source0_.eventId
            d_1_eventName_ = source0_.eventName
            return (m).set(d_0_eventId_, d_1_eventName_)

    @staticmethod
    def Normalize(m):
        return m


class Action:
    @classmethod
    def default(cls, ):
        return lambda: Action_PostEvent(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")))
    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)
    @property
    def is_PostEvent(self) -> bool:
        return isinstance(self, Action_PostEvent)

class Action_PostEvent(Action, NamedTuple('PostEvent', [('eventId', Any), ('eventName', Any)])):
    def __dafnystr__(self) -> str:
        return f'F3_2_REQ_4Domain.Action.PostEvent({self.eventId.VerbatimString(True)}, {self.eventName.VerbatimString(True)})'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_PostEvent) and self.eventId == __o.eventId and self.eventName == __o.eventName
    def __hash__(self) -> int:
        return super().__hash__()

