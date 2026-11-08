import sys
from typing import Callable, Any, TypeVar, NamedTuple
from math import floor
from itertools import count

import module_ as module_
import _dafny as _dafny
import System_ as System_

# Module: F3__2__REQ__7Domain

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
            if source0_.is_Add:
                d_0_k_ = source0_.key
                d_1_v_ = source0_.value
                return (m).set(d_0_k_, d_1_v_)
        if True:
            if source0_.is_Update:
                d_2_k_ = source0_.key
                d_3_v_ = source0_.value
                if (d_2_k_) in (m):
                    return (m).set(d_2_k_, d_3_v_)
                elif True:
                    return m
        if True:
            if source0_.is_Delete:
                d_4_k_ = source0_.key
                if (d_4_k_) in (m):
                    return (m) - (_dafny.Set({d_4_k_}))
                elif True:
                    return m
        if True:
            d_5_k_ = source0_.key
            return m

    @staticmethod
    def Normalize(m):
        return m


class Action:
    @classmethod
    def default(cls, ):
        return lambda: Action_Add(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")))
    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)
    @property
    def is_Add(self) -> bool:
        return isinstance(self, Action_Add)
    @property
    def is_Update(self) -> bool:
        return isinstance(self, Action_Update)
    @property
    def is_Delete(self) -> bool:
        return isinstance(self, Action_Delete)
    @property
    def is_Retrieve(self) -> bool:
        return isinstance(self, Action_Retrieve)

class Action_Add(Action, NamedTuple('Add', [('key', Any), ('value', Any)])):
    def __dafnystr__(self) -> str:
        return f'F3_2_REQ_7Domain.Action.Add({self.key.VerbatimString(True)}, {self.value.VerbatimString(True)})'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_Add) and self.key == __o.key and self.value == __o.value
    def __hash__(self) -> int:
        return super().__hash__()

class Action_Update(Action, NamedTuple('Update', [('key', Any), ('value', Any)])):
    def __dafnystr__(self) -> str:
        return f'F3_2_REQ_7Domain.Action.Update({self.key.VerbatimString(True)}, {self.value.VerbatimString(True)})'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_Update) and self.key == __o.key and self.value == __o.value
    def __hash__(self) -> int:
        return super().__hash__()

class Action_Delete(Action, NamedTuple('Delete', [('key', Any)])):
    def __dafnystr__(self) -> str:
        return f'F3_2_REQ_7Domain.Action.Delete({self.key.VerbatimString(True)})'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_Delete) and self.key == __o.key
    def __hash__(self) -> int:
        return super().__hash__()

class Action_Retrieve(Action, NamedTuple('Retrieve', [('key', Any)])):
    def __dafnystr__(self) -> str:
        return f'F3_2_REQ_7Domain.Action.Retrieve({self.key.VerbatimString(True)})'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_Retrieve) and self.key == __o.key
    def __hash__(self) -> int:
        return super().__hash__()

