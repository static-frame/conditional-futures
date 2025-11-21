import static_frame as sf


def duration_with_emoji(val: float) -> str:
    if val < 0.5:
        emoji = '🟢'
    elif val < 1.0:
        emoji = '🟡'
    else:
        emoji = '🔴'
    return f'{emoji} {val}'


if __name__ == '__main__':
    f = sf.FrameGO.from_records(
        [
            ['python3.14t', 'None', 0.577],
            ['python3.14t', 'ThreadPoolExecutor', 0.340],
            ['python3.14t', 'ConditionalThreadPoolExecutor', 0.339],
            ['python3.14', 'None', 0.544],
            ['python3.14', 'ThreadPoolExecutor', 2.231],
            ['python3.14', 'ConditionalThreadPoolExecutor', 0.532],
        ],
        columns=['Interpreter', 'Executor', 'Duration'],
    )
    f = f.assign['Duration'](f['Duration'].iter_element().apply(duration_with_emoji))

    config = sf.DisplayConfig(
        type_color=False, type_show=False, include_index=False, cell_max_width=100.0
    )

    print(f.to_markdown(config))
