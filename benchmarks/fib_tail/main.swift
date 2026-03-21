func fibAux(_ n: UInt64, _ a: UInt64, _ b: UInt64) -> UInt64 {
    if n == 0 {
        return a
    }
    return fibAux(n - 1, b, a + b)
}

func fib(_ n: UInt64) -> UInt64 {
    fibAux(n, 0, 1)
}

var sum: UInt64 = 0
let repeats: UInt64 = 100_000

for i in 0..<repeats {
    sum += fib(32 + (i % 2))
}

print(sum)
