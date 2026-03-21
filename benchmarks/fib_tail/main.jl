function fib_aux(n::UInt64, a::UInt64, b::UInt64)::UInt64
    if n == 0
        return a
    end
    return fib_aux(n - 1, b, a + b)
end

fib(n::UInt64) = fib_aux(n, UInt64(0), UInt64(1))

function main()
    println(fib(UInt64(32)))
end

main()
