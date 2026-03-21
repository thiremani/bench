total = 0.0
n = 10_000_001

for i in range(1, n):
    total += 1.0 / i

print(f"{total:.6f}")
