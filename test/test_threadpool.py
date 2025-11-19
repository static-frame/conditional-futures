from conditional_futures import ConditionalThreadPoolExecutor


def test_basic_map():
    def f(x):
        return x * 2

    with ConditionalThreadPoolExecutor(max_workers=4) as executor:
        result = list(executor.map(f, range(5)))
    assert result == [0, 2, 4, 6, 8]
