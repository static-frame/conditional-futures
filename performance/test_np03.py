import numpy as np
from np_common import main

NUMBER = 2
MAX_WORKERS = 8 # more workers helps here

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


# linux performance
# {.env314-condfut}{main} % python -m performance
# test_np01.py
#     python3.14
#          proc_single              1.311957
#          proc_thread_pool         3.796515
#          proc_cond_thread_pool    1.306277
#     python3.14t
#          proc_single              1.331948
#          proc_thread_pool         0.948886
#          proc_cond_thread_pool    0.95085
# test_np02.py
#     python3.14
#          proc_single              1.406858
#          proc_thread_pool         4.444127
#          proc_cond_thread_pool    1.479738
#     python3.14t
#          proc_single              1.435999
#          proc_thread_pool         1.044917
#          proc_cond_thread_pool    1.042418
# test_np03.py
#     python3.14
#          proc_single              34.665409
#          proc_thread_pool         37.356373
#          proc_cond_thread_pool    29.089636
#     python3.14t
#          proc_single              29.086205
#          proc_thread_pool         4.141262
#          proc_cond_thread_pool    4.153254