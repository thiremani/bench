sum = 0.0
n = 10_000_001

for i in range(1, n):
    sum += 1.0 / i

print(f"{sum:.6f}")
