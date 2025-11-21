import numpy as np
from np_common import main

NUMBER = 1
MAX_WORKERS = 8

array = np.arange(100_000_000).reshape(100_000, 1_000)

def func(row):
    s = 0.0
    c = 0.0
    for x in row:
        y = x - c
        t = s + y
        c = (t - s) - y
        s = t
    return s

if __name__ == '__main__':
    main(func, array, MAX_WORKERS, NUMBER)
