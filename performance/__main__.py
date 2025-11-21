import subprocess
from pathlib import Path

BINS = [
    Path.home() / '.env314-condfut' / 'bin' / 'python3.14',
    Path.home() / '.env314t-condfut' / 'bin' / 'python3.14',
]


if __name__ == '__main__':
    # Get the directory where this script is located
    performance_dir = Path(__file__).parent

    # Find all test_*.py modules in the directory
    test_modules = sorted(performance_dir.glob('perf_*.py'))

    # Run each test module with each executable
    for test_module in test_modules:
        print(f'{test_module.name}')

        for bin_path in BINS:
            is_ft = '314t' in str(bin_path)
            print(f'    {bin_path.name}{"t" if is_ft else ""}')

            try:
                result = subprocess.run(
                    [str(bin_path), str(test_module)],
                    cwd=performance_dir,
                    capture_output=False,
                )
                if result.returncode != 0:
                    print(
                        f'Warning: {test_module.name} exited with code {result.returncode}'
                    )
            except Exception as e:
                print(f'Error running {test_module.name} with {bin_path.name}: {e}')


# linux performance
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


# macos
# test_np01.py
#     python3.14
#          proc_single              0.519131
#          proc_thread_pool         1.84927
#          proc_cond_thread_pool    0.511398
#     python3.14t
#          proc_single              0.56307
#          proc_thread_pool         0.411119
#          proc_cond_thread_pool    0.40859
# test_np02.py
#     python3.14
#          proc_single              0.615515
#          proc_thread_pool         2.544554
#          proc_cond_thread_pool    0.611674
#     python3.14t
#          proc_single              0.654962
#          proc_thread_pool         0.50488
#          proc_cond_thread_pool    0.496363
# test_np03.py
#     python3.14
#          proc_single              17.16677
#          proc_thread_pool         17.614034
#          proc_cond_thread_pool    16.627494
#     python3.14t
#          proc_single              16.776953
#          proc_thread_pool         2.596718
#          proc_cond_thread_pool    2.611898
