function fib(n::UInt64)::UInt64
    if n <= 1
        return n
    end
    return fib(n - 1) + fib(n - 2)
end

function bench_output()
    return string(fib(UInt64(32)))
end

if abspath(PROGRAM_FILE) == @__FILE__
    println(bench_output())
end
