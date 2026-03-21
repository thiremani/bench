using Printf

function bench_output()
    acc = 0.0
    n = UInt64(10_000_001)

    for i in UInt64(1):(n - 1)
        acc += 1.0 / Float64(i)
    end

    return @sprintf("%.6f", acc)
end

if abspath(PROGRAM_FILE) == @__FILE__
    println(bench_output())
end
