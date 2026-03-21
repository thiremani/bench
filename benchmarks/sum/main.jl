function bench_output()
    acc = UInt64(0)
    n = UInt64(20_000_000)

    for i in UInt64(1):n
        acc += (i * UInt64(3)) % UInt64(17)
    end

    return string(acc)
end

if abspath(PROGRAM_FILE) == @__FILE__
    println(bench_output())
end
