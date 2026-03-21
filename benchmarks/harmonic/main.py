def bench_output() -> str:
    total = 0.0
    n = 10_000_001

    for i in range(1, n):
        total += 1.0 / i

    return f"{total:.6f}"


if __name__ == "__main__":
    print(bench_output())
