import numpy as np


CHUNK_SIZE = 1_000_000
N = 20_000_000


total = 0

for start in range(1, N + 1, CHUNK_SIZE):
    end = min(start + CHUNK_SIZE, N + 1)
    values = np.arange(start, end, dtype=np.int32)
    values *= 3
    values %= 17
    total += int(values.sum(dtype=np.int64))

print(total)
