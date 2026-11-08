import sys
from typing import Callable, Any, TypeVar, NamedTuple
from math import floor
from itertools import count

import module_ as module_
import _dafny as _dafny
import System_ as System_

# Module: F3__2__REQ__6Domain

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
            if source0_.is_AddStakeholder:
                d_0_name_ = source0_.name
                d_1_credentials_ = source0_.credentials
                return (m).set(d_0_name_, d_1_credentials_)
        if True:
            d_2_name_ = source0_.name
            return (m) - (_dafny.Set({d_2_name_}))

    @staticmethod
    def Normalize(m):
        return m


class Action:
    @classmethod
    def default(cls, ):
        return lambda: Action_AddStakeholder(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")), _dafny.Map({}))
    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)
    @property
    def is_AddStakeholder(self) -> bool:
        return isinstance(self, Action_AddStakeholder)
    @property
    def is_RemoveStakeholder(self) -> bool:
        return isinstance(self, Action_RemoveStakeholder)

class Action_AddStakeholder(Action, NamedTuple('AddStakeholder', [('name', Any), ('credentials', Any)])):
    def __dafnystr__(self) -> str:
        return f'F3_2_REQ_6Domain.Action.AddStakeholder({self.name.VerbatimString(True)}, {_dafny.string_of(self.credentials)})'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_AddStakeholder) and self.name == __o.name and self.credentials == __o.credentials
    def __hash__(self) -> int:
        return super().__hash__()

class Action_RemoveStakeholder(Action, NamedTuple('RemoveStakeholder', [('name', Any)])):
    def __dafnystr__(self) -> str:
        return f'F3_2_REQ_6Domain.Action.RemoveStakeholder({self.name.VerbatimString(True)})'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_RemoveStakeholder) and self.name == __o.name
    def __hash__(self) -> int:
        return super().__hash__()

