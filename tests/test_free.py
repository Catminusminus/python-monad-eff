from python_monad_eff.free import ListFunctor, Pure, Free, Join

def test_free():
    list_monad = Pure[ListFunctor[int]].pure(10)
    list_monad_2 = Join(ListFunctor[Free]([Pure(10), Pure(20)]))
    # Functor
    f = lambda x: x + 1
    g = lambda x: x * 2
    # Functor
    assert list_monad.fmap(lambda x: x) == list_monad
    assert list_monad.fmap(lambda x: f(g(x))) == list_monad.fmap(g).fmap(f)
    assert list_monad_2.fmap(lambda x: x) == list_monad_2
    assert list_monad_2.fmap(lambda x: f(g(x))) == list_monad_2.fmap(g).fmap(f)
