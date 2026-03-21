function run_sum()
    acc = UInt64(0)
    n = UInt64(20_000_000)

    for i in UInt64(1):n
        acc += (i * UInt64(3)) % UInt64(17)
    end

    return acc
end

println(run_sum())
