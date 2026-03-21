import Foundation

var sum = 0.0
let n: UInt64 = 10_000_001

for i in 1..<n {
    sum += 1.0 / Double(i)
}

print(String(format: "%.6f", sum))
