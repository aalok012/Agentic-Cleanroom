import sys
from typing import Callable, Any, TypeVar, NamedTuple
from math import floor
from itertools import count

import module_ as module_
import _dafny as _dafny
import System_ as System_

# Module: F4__2Domain

class default__:
    def  __init__(self):
        pass

    @staticmethod
    def Init():
        return (False, _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")))

    @staticmethod
    def Apply(m, a):
        source0_ = a
        if True:
            if source0_.is_Login:
                d_0_u_ = source0_.username
                d_1_p_ = source0_.password
                if ((d_0_u_) == (_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "validuser")))) and ((d_1_p_) == (_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "validpass")))):
                    return (True, d_0_u_)
                elif True:
                    return m
        if True:
            return m

    @staticmethod
    def Normalize(m):
        return m


class Action:
    @classmethod
    def default(cls, ):
        return lambda: Action_Login(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")))
    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)
    @property
    def is_Login(self) -> bool:
        return isinstance(self, Action_Login)
    @property
    def is_Prompt(self) -> bool:
        return isinstance(self, Action_Prompt)

class Action_Login(Action, NamedTuple('Login', [('username', Any), ('password', Any)])):
    def __dafnystr__(self) -> str:
        return f'F4_2Domain.Action.Login({self.username.VerbatimString(True)}, {self.password.VerbatimString(True)})'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_Login) and self.username == __o.username and self.password == __o.password
    def __hash__(self) -> int:
        return super().__hash__()

class Action_Prompt(Action, NamedTuple('Prompt', [])):
    def __dafnystr__(self) -> str:
        return f'F4_2Domain.Action.Prompt'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_Prompt)
    def __hash__(self) -> int:
        return super().__hash__()

