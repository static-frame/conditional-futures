import static_frame as sf

if __name__ == '__main__':
    f = sf.Frame.from_records([
        ['python3.14t', 'None', 0.577],
        ['python3.14t', 'ThreadPoolExecutor', 0.340],
        ['python3.14t', 'ConditionalThreadPoolExecutor', 0.339],
        ['python3.14', 'None', 0.544],
        ['python3.14', 'ThreadPoolExecutor', 2.231],
        ['python3.14', 'ConditionalThreadPoolExecutor', 0.532],
    ],
        columns=['Interpreter', 'Threading', 'Duration'],
        )


    config = sf.DisplayConfig(
        type_color=False,
        type_show=False,
        include_index=False,
        cell_max_width=100.
    )

    print(f.to_markdown(config))