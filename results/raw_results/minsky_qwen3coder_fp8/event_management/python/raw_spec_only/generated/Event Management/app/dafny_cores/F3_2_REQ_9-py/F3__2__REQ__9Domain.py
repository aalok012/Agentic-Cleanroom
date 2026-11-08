import sys
from typing import Callable, Any, TypeVar, NamedTuple
from math import floor
from itertools import count

import module_ as module_
import _dafny as _dafny
import System_ as System_

# Module: F3__2__REQ__9Domain

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
            if source0_.is_AddClient:
                d_0_id_ = source0_.id_
                return (m).set(d_0_id_, True)
        if True:
            d_1_id_ = source0_.id_
            if (d_1_id_) in (m):
                return (m) - (_dafny.Set({d_1_id_}))
            elif True:
                return m

    @staticmethod
    def Normalize(m):
        return m


class Action:
    @classmethod
    def default(cls, ):
        return lambda: Action_AddClient(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")))
    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)
    @property
    def is_AddClient(self) -> bool:
        return isinstance(self, Action_AddClient)
    @property
    def is_DeleteClient(self) -> bool:
        return isinstance(self, Action_DeleteClient)

class Action_AddClient(Action, NamedTuple('AddClient', [('id_', Any)])):
    def __dafnystr__(self) -> str:
        return f'F3_2_REQ_9Domain.Action.AddClient({self.id_.VerbatimString(True)})'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_AddClient) and self.id_ == __o.id_
    def __hash__(self) -> int:
        return super().__hash__()

class Action_DeleteClient(Action, NamedTuple('DeleteClient', [('id_', Any)])):
    def __dafnystr__(self) -> str:
        return f'F3_2_REQ_9Domain.Action.DeleteClient({self.id_.VerbatimString(True)})'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_DeleteClient) and self.id_ == __o.id_
    def __hash__(self) -> int:
        return super().__hash__()

