"""Tests memoizationtools.py"""

# pylint: disable=invalid-name

from memoizationtools.memoizationtools import MemoizedFunction, memoize


def identity_func(x):
    """Identity function."""
    return x


def compatability_function(*args, **kwargs):
    """A function that is compatible with any inputs."""
    return args, kwargs


def test_memoize_interface():
    """Tests that memoize preserves the interface of functions that it decorates."""

    func = memoize(compatability_function)

    assert func() == ((), {})
    assert func() == ((), {})
    assert func(1, 2, 3) == ((1, 2, 3), {})
    assert func(name="testing") == ((), {"name": "testing"})
    assert func(1, 2, 8, name="testing") == ((1, 2, 8), {"name": "testing"})


def test_MemoizedFunction_interface():
    """Tests that MemoizedFunction preserves the interface of functions that it decorates."""
    func = MemoizedFunction(compatability_function)

    assert func() == ((), {})
    assert func() == ((), {})
    assert func(1, 2, 3) == ((1, 2, 3), {})
    assert func(name="testing") == ((), {"name": "testing"})
    assert func(1, 2, 8, name="testing") == ((1, 2, 8), {"name": "testing"})


def test_MemoizedFunction_metadata():
    """Tests that MemoizedFunction collects the correct metadata and hits the cache."""
    func = MemoizedFunction(compatability_function)

    assert func.n_calls == 0
    assert func.cache_hits == 0

    func()
    func()
    func()
    func(1, 2, 3)

    assert func.n_calls == 4
    assert func.cache_hits == 2

    func(1, 2, 8, name="tester")
    func(1, 2, 8, name="tester")
    func(1, 2, 8, name="tester")

    assert func.n_calls == 7
    assert func.cache_hits == 4

    assert len(func.cache) == 3
