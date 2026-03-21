function fib_aux(n::UInt64, a::UInt64, b::UInt64)::UInt64
    if n == 0
        return a
    end
    return fib_aux(n - 1, b, a + b)
end

fib(n::UInt64) = fib_aux(n, UInt64(0), UInt64(1))

function main()
    acc = UInt64(0)
    repeats = UInt64(100_000)

    for i in UInt64(0):(repeats - 1)
        acc += fib(UInt64(32) + (i % UInt64(2)))
    end

    println(acc)
end

main()
