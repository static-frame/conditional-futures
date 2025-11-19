from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch

from conditional_futures import ConditionalThreadPoolExecutor
from conditional_futures.threadpool import SingleThreadExecutor


def test_basic_map():
    def f(x):
        return x * 2

    with ConditionalThreadPoolExecutor(max_workers=4) as executor:
        result = list(executor.map(f, range(5)))
    assert result == [0, 2, 4, 6, 8]


def test_gil_enabled_uses_single_thread_executor():
    """Test that SingleThreadExecutor is used when GIL is enabled."""
    with patch("conditional_futures.threadpool.IS_NO_GIL", False):
        with ConditionalThreadPoolExecutor(max_workers=4) as executor:
            assert isinstance(executor._executor, SingleThreadExecutor)
            assert not isinstance(executor._executor, ThreadPoolExecutor)


def test_gil_disabled_uses_thread_pool_executor():
    """Test that ThreadPoolExecutor is used when GIL is disabled."""
    with patch("conditional_futures.threadpool.IS_NO_GIL", True):
        with ConditionalThreadPoolExecutor(max_workers=4) as executor:
            assert isinstance(executor._executor, ThreadPoolExecutor)
            assert not isinstance(executor._executor, SingleThreadExecutor)


def test_gil_enabled_submit_works():
    """Test submit method works correctly with GIL enabled (SingleThreadExecutor)."""
    with patch("conditional_futures.threadpool.IS_NO_GIL", False):
        with ConditionalThreadPoolExecutor(max_workers=4) as executor:
            future = executor.submit(lambda x: x * 2, 5)
            assert future.result() == 10


def test_gil_disabled_submit_works():
    """Test submit method works correctly with GIL disabled (ThreadPoolExecutor)."""
    with patch("conditional_futures.threadpool.IS_NO_GIL", True):
        with ConditionalThreadPoolExecutor(max_workers=4) as executor:
            future = executor.submit(lambda x: x * 2, 5)
            assert future.result() == 10


def test_gil_enabled_map_works():
    """Test map method works correctly with GIL enabled (SingleThreadExecutor)."""
    with patch("conditional_futures.threadpool.IS_NO_GIL", False):
        with ConditionalThreadPoolExecutor(max_workers=4) as executor:
            result = list(executor.map(lambda x: x * 2, range(5)))
            assert result == [0, 2, 4, 6, 8]


def test_gil_disabled_map_works():
    """Test map method works correctly with GIL disabled (ThreadPoolExecutor)."""
    with patch("conditional_futures.threadpool.IS_NO_GIL", True):
        with ConditionalThreadPoolExecutor(max_workers=4) as executor:
            result = list(executor.map(lambda x: x * 2, range(5)))
            assert result == [0, 2, 4, 6, 8]


def test_gil_enabled_exception_handling():
    """Test exception handling with GIL enabled (SingleThreadExecutor)."""
    with patch("conditional_futures.threadpool.IS_NO_GIL", False):
        with ConditionalThreadPoolExecutor(max_workers=4) as executor:
            future = executor.submit(lambda: 1 / 0)
            try:
                future.result()
                assert False, "Should have raised ZeroDivisionError"
            except ZeroDivisionError:
                pass


def test_gil_disabled_exception_handling():
    """Test exception handling with GIL disabled (ThreadPoolExecutor)."""
    with patch("conditional_futures.threadpool.IS_NO_GIL", True):
        with ConditionalThreadPoolExecutor(max_workers=4) as executor:
            future = executor.submit(lambda: 1 / 0)
            try:
                future.result()
                assert False, "Should have raised ZeroDivisionError"
            except ZeroDivisionError:
                pass
