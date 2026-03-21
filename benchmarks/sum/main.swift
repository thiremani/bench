var sum: UInt64 = 0
let n: UInt64 = 100_000_000

for i in 1...n {
    sum += i
}

print(sum)
