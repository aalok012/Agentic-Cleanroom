import sys
from typing import Callable, Any, TypeVar, NamedTuple
from math import floor
from itertools import count

import module_ as module_
import _dafny as _dafny
import System_ as System_

# Module: F3__2Domain

class default__:
    def  __init__(self):
        pass

    @staticmethod
    def Init():
        return (False, _dafny.Set({}))

    @staticmethod
    def Apply(m, a):
        source0_ = a
        if True:
            d_0_eventId_ = source0_
            if (m)[0]:
                return (True, ((m)[1]) | (_dafny.Set({d_0_eventId_})))
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
    def is_RegisterForEvent(self) -> bool:
        return isinstance(self, Action_RegisterForEvent)

class Action_RegisterForEvent(Action, NamedTuple('RegisterForEvent', [('eventId', Any)])):
    def __dafnystr__(self) -> str:
        return f'F3_2Domain.Action.RegisterForEvent({self.eventId.VerbatimString(True)})'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_RegisterForEvent) and self.eventId == __o.eventId
    def __hash__(self) -> int:
        return super().__hash__()

