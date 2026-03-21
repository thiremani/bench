function fib(n::UInt64)::UInt64
    if n <= 1
        return n
    end
    return fib(n - 1) + fib(n - 2)
end

function main()
    println(fib(UInt64(32)))
end

main()
