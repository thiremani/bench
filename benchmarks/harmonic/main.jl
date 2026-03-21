using Printf

function main()
    acc = 0.0
    n = UInt64(10_000_001)

    for i in UInt64(1):(n - 1)
        acc += 1.0 / Float64(i)
    end

    @printf("%.6f\n", acc)
end

main()
