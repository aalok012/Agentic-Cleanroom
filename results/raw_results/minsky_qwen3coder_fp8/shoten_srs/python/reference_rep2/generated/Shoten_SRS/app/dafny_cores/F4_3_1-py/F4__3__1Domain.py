import sys
from typing import Callable, Any, TypeVar, NamedTuple
from math import floor
from itertools import count

import module_ as module_
import _dafny as _dafny
import System_ as System_

# Module: F4__3__1Domain

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
            let_tmp_rhs0_ = m
            d_0___v1_ = let_tmp_rhs0_[0]
            d_1_books_ = let_tmp_rhs0_[1]
            return (True, d_1_books_)

    @staticmethod
    def Normalize(m):
        return m


class Book:
    @classmethod
    def default(cls, ):
        return lambda: Book_Book(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")), int(0), False, _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "")))
    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)
    @property
    def is_Book(self) -> bool:
        return isinstance(self, Book_Book)

class Book_Book(Book, NamedTuple('Book', [('title', Any), ('author', Any), ('isbn', Any), ('price', Any), ('availability', Any), ('condition', Any), ('coverImage', Any)])):
    def __dafnystr__(self) -> str:
        return f'F4_3_1Domain.Book.Book({self.title.VerbatimString(True)}, {self.author.VerbatimString(True)}, {self.isbn.VerbatimString(True)}, {_dafny.string_of(self.price)}, {_dafny.string_of(self.availability)}, {self.condition.VerbatimString(True)}, {self.coverImage.VerbatimString(True)})'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Book_Book) and self.title == __o.title and self.author == __o.author and self.isbn == __o.isbn and self.price == __o.price and self.availability == __o.availability and self.condition == __o.condition and self.coverImage == __o.coverImage
    def __hash__(self) -> int:
        return super().__hash__()


class Action:
    @_dafny.classproperty
    def AllSingletonConstructors(cls):
        return [Action_SearchBook()]
    @classmethod
    def default(cls, ):
        return lambda: Action_SearchBook()
    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)
    @property
    def is_SearchBook(self) -> bool:
        return isinstance(self, Action_SearchBook)

class Action_SearchBook(Action, NamedTuple('SearchBook', [])):
    def __dafnystr__(self) -> str:
        return f'F4_3_1Domain.Action.SearchBook'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Action_SearchBook)
    def __hash__(self) -> int:
        return super().__hash__()

