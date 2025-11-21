# conditional-futures

Make multi-threaded concurrency backward- and forward-compatible for the free-threaded future of Python.


### Multi-Threading In and Out of Free-Threading

The following is a table of performance results for the execution of a function across each row of NumPy array, with `python3.14t` and `python3.14`, and with and without using a `ThreadPoolExecutor`. Performance improves with `python3.14t` but degrades with `python3.14`.

|Interpreter |Executor                      |Duration|
|------------|------------------------------|--------|
|python3.14t |None                          |🟡 0.577 |
|python3.14t |ThreadPoolExecutor            |🟢 0.34  |
|python3.14  |None                          |🟡 0.544 |
|python3.14  |ThreadPoolExecutor            |🔴 2.231 |

`ConditionalThreadPoolExecutor` lets a single interface get the best result in both contexts.

|Interpreter |Executor                      |Duration|
|------------|------------------------------|--------|
|python3.14t |None                          |🟡 0.577 |
|python3.14t |ConditionalThreadPoolExecutor |🟢 0.339 |
|python3.14  |None                          |🟡 0.544 |
|python3.14  |ConditionalThreadPoolExecutor |🟡 0.532 |


### Introduction

The new free-threaded version of Python (with the [GIL](https://docs.python.org/3/glossary.html#term-global-interpreter-lock) disabled) offers extraordinary improvement in performance of CPU-bound processes. Upgrading your code to take advantage of this performance, however, is problematic. The same multi-threaded code, if run with the GIL enabled, can actually perform significantly worse than single-threaded execution. Worse, even when using a free-threaded interpreter, importing an incompatible C-extension will automatically re-enable the GIL.

For code that will run in multiple interpreters, we need interfaces that perform multi-threaded processing only when the GIL is disabled.

The `conditional-futures` package provides `ConditionalThreadPoolExecutor`, a drop-in replacement for `ThreadPoolExecutor` that adapts based on the runtime state of the GIL.

When running under free-threaded Python with the GIL disabled `ConditionalThreadPoolExecutor` behaves like a normal thread pool. When running under a GIL-enabled build, it falls back on single-threaded execution, potentially avoiding a significant degradation in performance. The same implementation thus offers optimal performance in all contexts.

Note that, even with the GIL enabled, multi-threading can perform well for I/O-bound processes. `ConditionalThreadPoolExecutor` is appropriate only for CPU-bound processes that perform worse with the GIL.


### Example

Function application on the rows of a 2D NumPy array can prove the benefits of both free-threaded Python and the need for `ConditionalThreadPoolExecutor`.

First, using the free-threaded build of Python 3.14, we can create an array and apply a function to each row of that array. The `ipython` `%time` utility is used to measure duration.

```python
$ python3.14t
>>> import numpy as np
>>> array = np.arange(100_000_000).reshape(100_000, 1_000)
>>> func = lambda row: (row[row % 2 == 0]**2).sum()
>>> %time _ = np.fromiter((func(row) for row in array), dtype=float, count=array.shape[0])
CPU times: user 580 ms, sys: 662 μs, total: 580 ms
Wall time: 581 ms
```

Using `ConditionalThreadPoolExecutor` with this GIL-disabled build of Python we can take advantage of multi-threaded performance on a CPU-bound process: the same routine is almost twice as fast:

```python
>>> from conditional_futures import ConditionalThreadPoolExecutor
>>> with ConditionalThreadPoolExecutor(max_workers=4) as ex:
...     %time _ = np.fromiter(ex.map(func, array), dtype=float, count=array.shape[0])
...
CPU times: user 1.31 s, sys: 98 ms, total: 1.41 s
Wall time: 352 ms
```

Now, if using the standard Python 3.14 interpreter (with the GIL enabled), we can see detrimental performance using when using the standard `ThreadPoolExecutor`: the same operation takes six times as long!

```python
$ python3.14
>>> from concurrent.futures import ThreadPoolExecutor
>>> array = np.arange(100_000_000).reshape(100_000, 1_000)
>>> func = lambda row: (row[row % 2 == 0] ** 2).sum()
>>> with ThreadPoolExecutor(max_workers=4) as ex:
...     %time _ = np.fromiter(ex.map(func, array), dtype=float, count=array.shape[0])
...
CPU times: user 1.9 s, sys: 2.21 s, total: 4.12 s
Wall time: 2.33 s
```

Using `ConditionalThreadPoolExecutor` we can have one implementation that performs optimally in both contexts. Running the same code with the GIL enabled, `ConditionalThreadPoolExecutor` does not perform as well as in `python3.14t` but provides the best option available, single-threaded performance.


```python
>>> from conditional_futures import ConditionalThreadPoolExecutor
>>> with ConditionalThreadPoolExecutor(max_workers=4) as ex:
...     %time _ = np.fromiter(ex.map(func, array), dtype=float, count=array.shape[0])
...
CPU times: user 532 ms, sys: 773 μs, total: 533 ms
Wall time: 533 ms
```


### Installation

```bash
pip install conditional-futures
```

