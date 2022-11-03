from typing import Callable, Generic, TypeVar, List, Any

T = TypeVar("T")
U = TypeVar("U")


class Just(Generic[T]):
    value: T
    __match_args__ = ("value",)
    __slots__ = ("value",)

    def __init__(self, value: T) -> None:
        self.value = value

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Just) and self.value == other.value

    def __repr__(self) -> str:
        return f"Just({repr(self.value)})"

    def __ne__(self, other: Any) -> bool:
        return not (self == other)

    def fmap(self, f: Callable[[T], U]) -> "Just[U]":
        return Just(f(self.value))

    @staticmethod
    def pure(value: U) -> "Just[U]":
        return Just(value)

    def is_just(self) -> bool:
        return True

    # def ap(self, fv: "Just"[Callable[[T], U]] | "Nothing"):
    def ap(self, fv):
        match fv:
            case Nothing():
                return Nothing()
            case Just(value):
                return Just(value(self.value))

    def bind(self, fv):
        return fv(self.value)

class Nothing:
    def __init__(self) -> None:
        pass

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Nothing)

    def __repr__(self) -> str:
        return f"Nothing()"

    def __ne__(self, other: Any) -> bool:
        return not (self == other)

    def fmap(self, _: Callable) -> "Nothing":
        return self

    @staticmethod
    def pure(value: U) -> "Just[U]":
        return Just(value)

    def is_just(self) -> bool:
        return False

    def ap(self, _) -> "Nothing":
        return Nothing()

    def bind(self, _) -> "Nothing":
        return Nothing()

Maybe = Just[T] | Nothing

def flatten(l: List[List[T]]) -> List[T]:
    return [item for sublist in l for item in sublist]

class List_:
    def __init__(self, list: List[T]) -> None:
        self._list = list

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, List_) and self._list == other._list

    def __repr__(self) -> str:
        return f"List_({repr(self._list)})"

    def __ne__(self, other: Any) -> bool:
        return not (self == other)

    def fmap(self, f: Callable[[T], U]) -> "List_[U]":
        return List_([f(v) for v in self._list])

    @staticmethod
    def pure(value: U) -> "List_[U]":
        return List_([value])

    def ap(self, fv):
        return List_(flatten([[f(v) for f in fv._list] for v in self._list]))

    def bind(self, fv):
        return List_(flatten([fv(v)._list for v in self._list]))

M = TypeVar("M")

class MaybeT(Generic[M]):
    def __init__(self, value) -> None:
        self._mvalue = value

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, MaybeT) and self._mvalue == other._mvalue

    @staticmethod
    def runMaybeT(maybet):
        return maybet._mvalue

    def fmap(self, f):
        def run(v):
            match v:
                case Just(value):
                    return self._mvalue.pure(Just(f(value)))
                case Nothing():
                    return self._mvalue.pure(Nothing())
                case vv:
                    print(vv)
        return MaybeT[M](self._mvalue.bind(
            lambda v: run(v)
        ))

    @staticmethod
    def pure(cls: M, value): 
        return MaybeT[M](cls.pure(Just(value)))

    def ap(self, fv):
        def run(mf):
            def run2(v):
                match v:
                    case Nothing():
                        return M.pure(Nothing())
                    case Just(arg):
                        return M.pure(Just(f(arg)))

            match mf:
                case Nothing():
                    return M.pure(Nothing())
                case Just(f):
                    # runMaybeT[M](self)
                    return self._mvalue.bind(
                        lambda v: run2(v)
                    )
        return MaybeT[M](fv.bind(
            lambda mf: run(mf)
        ))

    def bind(self, fv):
        def run(v):
            match v:
                case Nothing():
                    return M.pure(Nothing())
                case Just(arg):
                    return MaybeT[M].runMaybeT(fv(arg))
        # runMaybeT[M](self)
        return MaybeT[M](self._mvalue.bind(
            lambda v: run(v)
        ))

    def list(self, mv: M):
        return MaybeT[M](mv.fmap(lambda v: Just(v)))
