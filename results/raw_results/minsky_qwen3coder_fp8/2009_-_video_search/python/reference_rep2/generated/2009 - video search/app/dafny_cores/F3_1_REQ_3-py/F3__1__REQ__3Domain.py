import sys
from typing import Callable, Any, TypeVar, NamedTuple
from math import floor
from itertools import count

import module_ as module_
import _dafny as _dafny
import System_ as System_

# Module: F3__1__REQ__3Domain

class default__:
    def  __init__(self):
        pass

    @staticmethod
    def Init():
        return False

    @staticmethod
    def Apply(m, a):
        source0_ = a
        if True:
            d_0_enabled_ = source0_
            return d_0_enabled_

    @staticmethod
    def Normalize(m):
        return m


class Action:
    @classmethod
    def default(cls, ):
        return lambda: False
    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)
    @property
    def is_SetTorrentSearchEnabled(self) -> bool:
        return isinstance(self, Action_SetTorrentSearchEnabled)

class Action_SetTorrentSearchEnabled(Action, NamedTuple('SetTorrentSearchEnabled', [('enabled', Any)])):
    def __dafnystr__(self) -> str:
        return f'F3_1_REQ_3Domain.Action.SetTorrentSearchEnabled({_dafny.string_of(self.enabled)})'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_SetTorrentSearchEnabled) and self.enabled == __o.enabled
    def __hash__(self) -> int:
        return super().__hash__()

