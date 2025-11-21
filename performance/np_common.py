from concurrent.futures import ThreadPoolExecutor
import numpy as np
from conditional_futures import ConditionalThreadPoolExecutor
import timeit


def proc_single(func, array, max_workers):
    _ = np.fromiter((func(row) for row in array), dtype=float, count=array.shape[0])

def proc_thread_pool(func, array, max_workers):
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        _ = np.fromiter(ex.map(func, array), dtype=float, count=array.shape[0])

def proc_cond_thread_pool(func, array, max_workers):
    with ConditionalThreadPoolExecutor(max_workers=max_workers) as ex:
        _ = np.fromiter(ex.map(func, array), dtype=float, count=array.shape[0])


def main(func, array, max_workers, number):
    for proc in (proc_single, proc_thread_pool, proc_cond_thread_pool):
        result = timeit.timeit(f'proc(func, array, max_workers)', globals=locals(), number=number)
        print(' ' * 8, proc.__name__.ljust(24), round(result / number, 6))
