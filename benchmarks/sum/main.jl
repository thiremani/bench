function main()
    acc = UInt64(0)
    n = UInt64(100_000_000)

    for i in UInt64(1):n
        acc += i
    end

    println(acc)
end

main()
