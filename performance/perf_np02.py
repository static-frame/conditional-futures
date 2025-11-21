import numpy as np
from np_common import main

NUMBER = 4
MAX_WORKERS = 2

array = np.arange(100_000_000).reshape(100_000, 1_000)


# Shannon entropy
def func(row):
    p = row / row.sum()
    return -(p * np.log(p + 1e-12)).sum()


if __name__ == '__main__':
    main(func, array, MAX_WORKERS, NUMBER)
