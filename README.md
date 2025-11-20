# conditional-futures

Make multi-threaded concurrency backward- and forward-compatible for the free-threaded future of Python.


---

### Introduction

The new free-threaded version of Python (with the [GIL](https://docs.python.org/3/glossary.html#term-global-interpreter-lock) disabled) offers extraordinary improvement in performance of CPU-bound processes. Upgrading your code to take advantage of this performance, however, is problematic. The same multi-threaded code, if run with the GIL enabled, can actually perform significantly worse than single-threaded execution. Worse, even when using a free-threaded interpreter, importing an incompatible C-extension will automatically re-enable the GIL. For code that will run in multiple interpreters, we need interfaces that perform multi-threaded processing only when the GIL is disabled.

The `conditional-futures` package provides `ConditionalThreadPoolExecutor`, a drop-in replacement for `ThreadPoolExecutor` that adapts based on the runtime state of the GIL. When running under free-threaded Python with the GIL disabled it behaves like a normal thread pool. When running under a GIL-enabled build, it falls back on single-threaded execution, potentially protecting the user from a significant degradation in performance. The same implementation thus offers optimal performance in all contexts.

Note that, even with the GIL enabled, Python multi-threading performs well for I/O-bound processes. `ConditionalThreadPoolExecutor` is appropriate only for CPU-bound processes that perform worse with the GIL.


### Example

Function application on the rows of a 2D NumPy array prove the benefits of free-threaded Python and the need for `ConditionalThreadPoolExecutor`.

First, using the free-threaded build of Python 3.14, we can create an array and apply a function to each row of that array. The `ipython` `%time` utility is used to measure duration.

```python
$ python3.14t
>>> import numpy as np
>>> array = np.arange(100_000_000).reshape(1_000, 100_000)
>>> func = lambda row: (row[row % 2 == 0]**2).sum()
>>> %time _ = np.fromiter((func(row) for row in array), dtype=float, count=array.shape[0])
CPU times: user 308 ms, sys: 36.4 ms, total: 345 ms
Wall time: 345 ms
```

Using `ConditionalThreadPoolExecutor` with this GIL-disabled build of Python we can take advantage of multi-threaded performance on a CPU-bound process: the same routine is now an order of magnitude faster:

```python
>>> from conditional_futures import ConditionalThreadPoolExecutor
>>> with ConditionalThreadPoolExecutor() as ex:
...     %time _ = np.fromiter(ex.map(func, array), dtype=float, count=array.shape[0])
...
CPU times: user 389 ms, sys: 29.1 ms, total: 418 ms
Wall time: 28.9 ms
```


### Installation

```bash
pip install conditional-futures
```

