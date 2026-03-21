def bench_output() -> str:
    total = 0
    n = 20_000_000

    for i in range(1, n + 1):
        total += (i * 3) % 17

    return str(total)


if __name__ == "__main__":
    print(bench_output())
