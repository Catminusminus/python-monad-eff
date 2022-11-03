from python_monad_eff.monad import Just, Nothing, List_, MaybeT

def test_maybe():
    f = lambda x: x + 1
    g = lambda x: x * 2
    # Functor
    assert Just(10).fmap(lambda x: x) == Just(10)
    assert Just(10).fmap(lambda x: f(g(x))) == Just(10).fmap(g).fmap(f)
    assert Nothing() == Nothing()
    assert Nothing().fmap(lambda x: f(g(x))) == Nothing().fmap(g).fmap(f)

    # Applicative

    # Monad
    assert Just.pure(10).bind(lambda x: Just(x + 1)) == (lambda x: Just(x + 1))(10)
    assert Just(10).bind(lambda x: Just.pure(x)) == Just(10)
    assert Just(10).bind(lambda x: Just(x + 1)).bind(lambda x: Just(x * 2)) == Just(10).bind(lambda x: (lambda x_: Just(x_ + 1))(x).bind(lambda x: Just(x * 2)))

    # Pattern Match
    a = Just([10])
    match a:
        case Just(value):
            assert value == [10]
        case _:
            assert False


def test_list():
    f = lambda x: x + 1
    g = lambda x: x * 2
    # Functor
    assert List_([10]).fmap(lambda x: x) == List_([10])
    assert List_([10]).fmap(lambda x: f(g(x))) == List_([10]).fmap(g).fmap(f)



def test_maybet():
    f = lambda x: x + 1
    g = lambda x: x * 2
    # Functor
    pure = lambda x: MaybeT[List_].pure(List_, x)
    assert pure(10).fmap(lambda x: x) == pure(10)
    assert pure(10).fmap(g).fmap(f) == pure(10).fmap(lambda x: f(g(x)))

    # Monad
    assert pure(10).bind(lambda x: pure(x + 1)) == (lambda x: pure(x + 1))(10)
    assert pure(10).bind(lambda x: pure(x)) == pure(10)
    assert pure(10).bind(lambda x: pure(x + 1)).bind(lambda x: pure(x * 2)) == pure(10).bind(lambda x: (lambda x_: pure(x_ + 1))(x).bind(lambda x: pure(x * 2)))

