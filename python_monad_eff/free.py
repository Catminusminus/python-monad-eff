from typing import Callable, Generic, TypeVar, List, Any, Union

T = TypeVar("T")
U = TypeVar("U")



class Pure(Generic[T]):
    value: T
    __match_args__ = ("value",)
    __slots__ = ("value",)

    def __init__(self, value: T) -> None:
        self.value = value

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Pure) and self.value == other.value

    def __repr__(self) -> str:
        return f"Pure({repr(self.value)})"

    def __ne__(self, other: Any) -> bool:
        return not (self == other)

    def fmap(self, f: Callable[[T], U]) -> "Pure[U]":
        return Pure(f(self.value))

    @staticmethod
    def pure(value: U) -> "Pure[U]":
        return Pure(value)

    # def ap(self, fv: "Pure"[Callable[[T], U]] | "Join"):
    def ap(self, fv):
        match fv:
            case Pure(value):
                return self.fmap(value)
            case Join(value):
                return Join(value.fmap(lambda v: self.ap(v)))

    def bind(self, fv):
        return fv(self.value)


class Join(Generic[T]):
    value: T
    __match_args__ = ("value",)
    __slots__ = ("value",)

    def __init__(self, value: T) -> None:
        self.value = value

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Join) and self.value == other.value

    def __repr__(self) -> str:
        return f"Join({repr(self.value)})"

    def __ne__(self, other: Any) -> bool:
        return not (self == other)

    def fmap(self, f: Callable[[T], U]) -> "Pure[U]":
        return Join(self.value.fmap(lambda v: v.fmap(f)))

    @staticmethod
    def pure(value: U) -> "Pure[U]":
        return Pure(value)

    #def ap(self, fv: "Pure"[Callable[[T], U]] | "Join"):
    def ap(self, fv):
        match fv:
            case Pure(value):
                return self.fmap(value)
            case Join(value):
                return Join(value.fmap(lambda v: self.ap(v)))

    def bind(self, fv):
        return Join(self.value.fmap(lambda v: v.bind(fv)))


A = TypeVar("A")

Free = Union[Pure[A], Join]


def flatten(l: List[List[T]]) -> List[T]:
    return [item for sublist in l for item in sublist]

class ListFunctor(Generic[T]):
    def __init__(self, list: List[T]) -> None:
        self._list = list

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, ListFunctor) and self._list == other._list

    def __repr__(self) -> str:
        return f"List_({repr(self._list)})"

    def __ne__(self, other: Any) -> bool:
        return not (self == other)

    def fmap(self, f: Callable[[T], U]) -> "ListFunctor[U]":
        return ListFunctor([f(v) for v in self._list])

    #@staticmethod
    #def pure(value: U) -> "List_[U]":
    #    return List_([value])

