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
        return (_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")), False, _dafny.Map({}))

    @staticmethod
    def Apply(m, a):
        source0_ = a
        if True:
            d_0_adminId_ = source0_.adminId
            d_1_clientId_ = source0_.clientId
            let_tmp_rhs0_ = m
            d_2_currentAdminId_ = let_tmp_rhs0_[0]
            d_3_currentHasAccess_ = let_tmp_rhs0_[1]
            d_4_clientData_ = let_tmp_rhs0_[2]
            if ((d_2_currentAdminId_) == (d_0_adminId_)) and (d_3_currentHasAccess_):
                return (d_0_adminId_, True, d_4_clientData_)
            elif True:
                return (d_0_adminId_, False, d_4_clientData_)

    @staticmethod
    def Normalize(m):
        return m


class Action:
    @classmethod
    def default(cls, ):
        return lambda: Action_AccessClientData(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")))
    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)
    @property
    def is_AccessClientData(self) -> bool:
        return isinstance(self, Action_AccessClientData)

class Action_AccessClientData(Action, NamedTuple('AccessClientData', [('adminId', Any), ('clientId', Any)])):
    def __dafnystr__(self) -> str:
        return f'F3_2_REQ_8Domain.Action.AccessClientData({self.adminId.VerbatimString(True)}, {self.clientId.VerbatimString(True)})'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_AccessClientData) and self.adminId == __o.adminId and self.clientId == __o.clientId
    def __hash__(self) -> int:
        return super().__hash__()

