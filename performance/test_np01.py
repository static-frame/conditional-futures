import timeit
from concurrent.futures import ThreadPoolExecutor

import numpy as np

from conditional_futures import ConditionalThreadPoolExecutor

NUMBER = 10
MAX_WORKERS = 2

# array = np.arange(100_000_000).reshape(1_000, 100_000)
array = np.arange(100_000_000).reshape(100_000, 1_000)
func = lambda row: (row[row % 2 == 0] ** 2).sum()


def proc_single():
    _ = np.fromiter((func(row) for row in array), dtype=float, count=array.shape[0])


def proc_thread_pool():
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        _ = np.fromiter(ex.map(func, array), dtype=float, count=array.shape[0])


def proc_cond_thread_pool():
    with ConditionalThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        _ = np.fromiter(ex.map(func, array), dtype=float, count=array.shape[0])


if __name__ == '__main__':
    for proc in (proc_single, proc_thread_pool, proc_cond_thread_pool):
        result = timeit.timeit(f'proc()', globals=locals(), number=NUMBER)
        print('\t', proc.__name__.ljust(24), round(result, 6))
