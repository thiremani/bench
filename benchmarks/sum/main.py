total = 0
n = 20_000_000

for i in range(1, n + 1):
    total += (i * 3) % 17

print(total)
