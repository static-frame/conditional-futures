# conditional-futures

Make multi-threaded concurrency backward- and forward-compatible for the free-threaded future of Python.


---

### Introduction

`ConditionalThreadPoolExecutor` is a drop-in replacement for `ThreadPoolExecutor`
that adapts to the runtime environment. When running under free-threaded Python with the GIL disabled (3.14t) it behaves like a normal thread pool. However, when running under a GIL-enabled build, it falls back on single-threaded execution.

The reason this is necessary is that CPU-bound processes that use multi-threading with the GIL can be much slower than single-threaded execution.
`ConditionalThreadPoolExecutor` permits having a single implementation that will perform optimally regardless of if the GIL is enabled or not.


### Why?

In CPython, the Global Interpreter Lock (GIL) prevents Python bytecode
from running truly concurrently on multiple threads.

ConditionalThreadPoolExecutor detects when threads will be ineffective and avoids spawning them. That means your code remains correct and fast on both GIL and no-GIL Python builds.

### Example

```python
>>> import numpy as np
>>> array = np.arange(100_000_000).reshape(100_000, 1_000)
>>> func = lambda row: (row[row % 2 == 0]**2).sum()
>>> with ConditionalThreadPoolExecutor(max_workers=22) as ex:
...     %time _ = np.fromiter(ex.map(func, array), dtype=float, count=array.shape[0])
...
CPU times: user 1.35 s, sys: 0 ns, total: 1.35 s
Wall time: 1.35 s
>>> with ThreadPoolExecutor(max_workers=22) as ex:
...     %time _ = np.fromiter(ex.map(func, array), dtype=float, count=array.shape[0])
...
CPU times: user 6.69 s, sys: 2.33 s, total: 9.02 s
Wall time: 6.02 s

```


```python
from conditional_futures import ConditionalThreadPoolExecutor

def work(x):
    return x * x

with ConditionalThreadPoolExecutor(max_workers=8) as executor:
    results = list(executor.map(work, range(10)))

print(results)
```

### Installation

```bash
pip install conditional-futures
```

