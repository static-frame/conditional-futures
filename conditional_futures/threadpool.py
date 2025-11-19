import sys
from concurrent.futures import Executor, Future, ThreadPoolExecutor
from typing import Callable, Iterable, Iterator, Optional, TypeVar

TVArgs = TypeVar("TVArgs")
TVReturn = TypeVar("TVReturn")


def is_no_gil() -> bool:
    if f := getattr(sys, "_is_gil_enabled", None):
        return not f()
    return False


IS_NO_GIL = is_no_gil()


class SingleThreadExecutor(Executor):
    """Executor that executes tasks synchronously in the calling thread."""

    def submit(
        self,
        fn: Callable[..., TVReturn],
        /,
        *args,
        **kwargs,
    ) -> Future:
        fut: Future = Future()
        try:
            fut.set_result(fn(*args, **kwargs))
        except Exception as e:
            fut.set_exception(e)
        return fut

    def map(
        self,
        fn: Callable[[TVArgs], TVReturn],
        *iterables: Iterable[TVArgs],
        timeout: Optional[float] = None,
        chunksize: int = 1,
        buffersize: int | None = None,
    ) -> Iterator[TVReturn]:
        return map(fn, *iterables)

    def shutdown(
        self,
        wait: bool = True,
        *,
        cancel_futures: bool = False,
    ) -> None:
        pass


class ConditionalThreadPoolExecutor(Executor):
    """
    Drop-in replacement for ThreadPoolExecutor
    """

    def __init__(
        self,
        max_workers: Optional[int] = None,
        **kwargs,
    ):
        self._max_workers = max_workers
        self._kwargs = kwargs
        self._executor: Executor

    def __enter__(self):
        self._executor = (
            ThreadPoolExecutor(max_workers=self._max_workers, **self._kwargs)
            if IS_NO_GIL
            else SingleThreadExecutor()
        )
        return self

    def submit(
        self,
        fn: Callable[..., TVReturn],
        /,
        *args,
        **kwargs,
    ) -> Future:
        return self._executor.submit(
            fn,
            *args,
            **kwargs,
        )

    def map(
        self,
        fn: Callable[[TVArgs], TVReturn],
        *iterables: Iterable[TVArgs],
        timeout: Optional[float] = None,
        chunksize: int = 1,
        buffersize: int | None = None,
    ) -> Iterator[TVReturn]:
        return self._executor.map(
            fn,
            *iterables,
            timeout=timeout,
            chunksize=chunksize,
            buffersize=buffersize,
        )

    def shutdown(
        self,
        wait: bool = True,
        *,
        cancel_futures: bool = False,
    ) -> None:
        self._executor.shutdown(
            wait,
            cancel_futures=cancel_futures,
        )
