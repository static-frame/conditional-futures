from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Callable, Iterable, Iterator, Any, Optional, TypeVar
import concurrent.futures as cf
import sys


def is_no_gil() -> bool:
    if hasattr(sys, '_is_gil_enabled'):
        return not sys._is_gil_enabled()
    return False


T = TypeVar("T")
R = TypeVar("R")

class _DirectExecutor:
    """Minimal Executor that runs tasks synchronously in the caller thread."""
    def submit(self, fn: Callable[..., R], /, *args: Any, **kwargs: Any) -> Future:
        fut: Future = Future()
        try:
            res = fn(*args, **kwargs)
        except BaseException as e:
            fut.set_exception(e)
        else:
            fut.set_result(res)
        return fut

    def map(
        self,
        fn: Callable[[T], R],
        *iterables: Iterable[T],
        timeout: Optional[float] = None,
        chunksize: int = 1,  # kept for API compat; ignored here
    ) -> Iterator[R]:
        # Synchronous map; raises as soon as fn raises.
        for args in zip(*iterables):
            yield fn(*args)

    def shutdown(self, wait: bool = True, *, cancel_futures: bool = False) -> None:
        return  # nothing to do


class ConditionalThreadPoolExecutor:
    """
    Context manager with the same shape as ThreadPoolExecutor.
    Uses real threads only if is_no_gil() is True; otherwise runs inline.
    """
    def __init__(self, max_workers: Optional[int] = None, **tp_kwargs: Any) -> None:
        self._max_workers = max_workers
        self._tp_kwargs = tp_kwargs
        self._executor: Any = None  # ThreadPoolExecutor | _DirectExecutor

    def __enter__(self) -> "ConditionalThreadPoolExecutor":
        if is_no_gil():  # <-- your predicate called here
            self._executor = ThreadPoolExecutor(max_workers=self._max_workers, **self._tp_kwargs)
        else:
            self._executor = _DirectExecutor()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        # Mirror ThreadPoolExecutor behavior
        self.shutdown(wait=True)

    # Delegate the common Executor API:
    def submit(self, fn: Callable[..., R], /, *args: Any, **kwargs: Any) -> Future:
        return self._executor.submit(fn, *args, **kwargs)

    def map(
        self,
        fn: Callable[[T], R],
        *iterables: Iterable[T],
        timeout: Optional[float] = None,
        chunksize: int = 1,
    ) -> Iterator[R]:
        # ThreadPoolExecutor.map supports timeout & chunksize; _Direct ignores chunksize.
        if isinstance(self._executor, ThreadPoolExecutor):
            return self._executor.map(fn, *iterables, timeout=timeout, chunksize=chunksize)
        return self._executor.map(fn, *iterables, timeout=timeout, chunksize=chunksize)

    def shutdown(self, wait: bool = True, *, cancel_futures: bool = False) -> None:
        self._executor.shutdown(wait=wait, cancel_futures=cancel_futures)
