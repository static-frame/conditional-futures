import numpy as np
from np_common import main

NUMBER = 4
MAX_WORKERS = 4

# array = np.arange(100_000_000).reshape(1_000, 100_000)
array = np.arange(100_000_000).reshape(100_000, 1_000)
func = lambda row: (row[row % 2 == 0] ** 2).sum()


if __name__ == '__main__':
    main(func, array, MAX_WORKERS, NUMBER)
