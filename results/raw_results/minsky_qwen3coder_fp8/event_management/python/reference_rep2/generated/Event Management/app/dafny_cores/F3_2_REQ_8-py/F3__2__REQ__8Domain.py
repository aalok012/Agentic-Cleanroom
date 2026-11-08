import sys
from typing import Callable, Any, TypeVar, NamedTuple
from math import floor
from itertools import count

import module_ as module_
import _dafny as _dafny
import System_ as System_

# Module: F3__2__REQ__8Domain

class default__:
    def  __init__(self):
        pass

    @staticmethod
    def Init():
        return (False, _dafny.Map({}))

    @staticmethod
    def Apply(m, a):
        source0_ = a
        if True:
            if source0_.is_AccessClientData:
                if (m)[0]:
                    return (True, (m)[1])
                elif True:
                    return (False, (m)[1])
        if True:
            if (m)[0]:
                return (True, (m)[1])
            elif True:
                return (False, (m)[1])

    @staticmethod
    def Normalize(m):
        return m


class Action:
    @_dafny.classproperty
    def AllSingletonConstructors(cls):
        return [Action_AccessClientData(), Action_ModifyClientData()]
    @classmethod
    def default(cls, ):
        return lambda: Action_AccessClientData()
    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)
    @property
    def is_AccessClientData(self) -> bool:
        return isinstance(self, Action_AccessClientData)
    @property
    def is_ModifyClientData(self) -> bool:
        return isinstance(self, Action_ModifyClientData)

class Action_AccessClientData(Action, NamedTuple('AccessClientData', [])):
    def __dafnystr__(self) -> str:
        return f'F3_2_REQ_8Domain.Action.AccessClientData'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_AccessClientData)
    def __hash__(self) -> int:
        return super().__hash__()

class Action_ModifyClientData(Action, NamedTuple('ModifyClientData', [])):
    def __dafnystr__(self) -> str:
        return f'F3_2_REQ_8Domain.Action.ModifyClientData'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_ModifyClientData)
    def __hash__(self) -> int:
        return super().__hash__()

