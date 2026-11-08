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
            if source0_.is_DataEntry:
                return m
        if True:
            if source0_.is_DataOrganization:
                return m
        if True:
            if source0_.is_DataRetrieval:
                return m
        if True:
            if source0_.is_DataModification:
                return m
        if True:
            return m

    @staticmethod
    def Normalize(m):
        return m


class Action:
    @_dafny.classproperty
    def AllSingletonConstructors(cls):
        return [Action_DataEntry(), Action_DataOrganization(), Action_DataRetrieval(), Action_DataModification(), Action_DataDeletion()]
    @classmethod
    def default(cls, ):
        return lambda: Action_DataEntry()
    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)
    @property
    def is_DataEntry(self) -> bool:
        return isinstance(self, Action_DataEntry)
    @property
    def is_DataOrganization(self) -> bool:
        return isinstance(self, Action_DataOrganization)
    @property
    def is_DataRetrieval(self) -> bool:
        return isinstance(self, Action_DataRetrieval)
    @property
    def is_DataModification(self) -> bool:
        return isinstance(self, Action_DataModification)
    @property
    def is_DataDeletion(self) -> bool:
        return isinstance(self, Action_DataDeletion)

class Action_DataEntry(Action, NamedTuple('DataEntry', [])):
    def __dafnystr__(self) -> str:
        return f'F3_2_REQ_7Domain.Action.DataEntry'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_DataEntry)
    def __hash__(self) -> int:
        return super().__hash__()

class Action_DataOrganization(Action, NamedTuple('DataOrganization', [])):
    def __dafnystr__(self) -> str:
        return f'F3_2_REQ_7Domain.Action.DataOrganization'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_DataOrganization)
    def __hash__(self) -> int:
        return super().__hash__()

class Action_DataRetrieval(Action, NamedTuple('DataRetrieval', [])):
    def __dafnystr__(self) -> str:
        return f'F3_2_REQ_7Domain.Action.DataRetrieval'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_DataRetrieval)
    def __hash__(self) -> int:
        return super().__hash__()

class Action_DataModification(Action, NamedTuple('DataModification', [])):
    def __dafnystr__(self) -> str:
        return f'F3_2_REQ_7Domain.Action.DataModification'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_DataModification)
    def __hash__(self) -> int:
        return super().__hash__()

class Action_DataDeletion(Action, NamedTuple('DataDeletion', [])):
    def __dafnystr__(self) -> str:
        return f'F3_2_REQ_7Domain.Action.DataDeletion'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_DataDeletion)
    def __hash__(self) -> int:
        return super().__hash__()

