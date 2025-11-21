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
    test_modules = sorted(performance_dir.glob('test_*.py'))

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
