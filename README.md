# conditional-futures

Make multi-threaded concurrency backward- and forward-compatible for the free-threaded future of Python.


---

### What?

`ConditionalThreadPoolExecutor` is a drop-in replacement for `ThreadPoolExecutor`
that automatically adapts to the runtime environment.

When running under **free-threaded Python (3.13t)** or when threads
are actually useful, it behaves like a normal thread pool.

When running under a traditional GIL build, it **falls back to single-threaded**
execution to avoid detrimental thread overhead.

### Why?

In CPython, the Global Interpreter Lock (GIL) prevents Python bytecode
from running truly concurrently on multiple threads.

ConditionalThreadPoolExecutor detects when threads will be ineffective and avoids spawning them. That means your code remains correct and fast on both GIL and no-GIL Python builds.

---

### Example

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

