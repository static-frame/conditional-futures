from __future__ import annotations
from concurrent.futures import Executor, ThreadPoolExecutor, Future
from typing import Callable, Iterable, Iterator, Optional, Any, TypeVar
import sys


def is_no_gil() -> bool:
    if hasattr(sys, '_is_gil_enabled'):
        return not sys._is_gil_enabled()
    return False


T = TypeVar("T")
R = TypeVar("R")


class _DirectExecutor(Executor):
    """Executor that executes tasks synchronously in the calling thread."""
    def submit(self, fn: Callable[..., R], /, *args, **kwargs) -> Future:
        fut: Future = Future()
        try:
            fut.set_result(fn(*args, **kwargs))
        except Exception as e:
            fut.set_exception(e)
        return fut

    def map(
        self,
        fn: Callable[[T], R],
        *iterables: Iterable[T],
        timeout: Optional[float] = None,
        chunksize: int = 1,
    ) -> Iterator[R]:
        return map(fn, *iterables)

    def shutdown(self, wait: bool = True, *, cancel_futures: bool = False) -> None:
        pass


class ConditionalThreadPoolExecutor(Executor):
    """
    Drop-in replacement for ThreadPoolExecutor that uses threads only when
    the runtime permits (e.g., no GIL, or other safe conditions).
    """
    def __init__(self, max_workers: Optional[int] = None, **kwargs):
        self._max_workers = max_workers
        self._kwargs = kwargs
        self._executor: Executor | None = None

    def __enter__(self):
        if is_no_gil():
            self._executor = ThreadPoolExecutor(max_workers=self._max_workers, **self._kwargs)
        else:
            self._executor = _DirectExecutor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown()

    def submit(self, fn: Callable[..., R], /, *args, **kwargs) -> Future:
        return self._executor.submit(fn, *args, **kwargs)

    def map(
        self,
        fn: Callable[[T], R],
        *iterables: Iterable[T],
        timeout: Optional[float] = None,
        chunksize: int = 1,
    ) -> Iterator[R]:
        return self._executor.map(fn, *iterables, timeout=timeout, chunksize=chunksize)

    def shutdown(self, wait: bool = True, *, cancel_futures: bool = False) -> None:
        self._executor.shutdown(wait=wait, cancel_futures=cancel_futures)
