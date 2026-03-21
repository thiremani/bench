def fib_aux(n: int, a: int, b: int) -> int:
    if n == 0:
        return a
    return fib_aux(n - 1, b, a + b)


def fib(n: int) -> int:
    return fib_aux(n, 0, 1)


print(fib(32))
