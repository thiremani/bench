func fibAux(_ n: UInt64, _ a: UInt64, _ b: UInt64) -> UInt64 {
    if n == 0 {
        return a
    }
    return fibAux(n - 1, b, a + b)
}

func fib(_ n: UInt64) -> UInt64 {
    fibAux(n, 0, 1)
}

print(fib(32))
