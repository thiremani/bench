import numpy as np


CHUNK_SIZE = 1_000_000
N = 10_000_000


total = 0.0

for start in range(1, N + 1, CHUNK_SIZE):
    end = min(start + CHUNK_SIZE, N + 1)
    values = np.arange(start, end, dtype=np.float64)
    np.reciprocal(values, out=values)
    total += float(values.sum(dtype=np.float64))

print(f"{total:.6f}")
