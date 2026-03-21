#include <stdint.h>
#include <stdio.h>

static uint64_t fib_aux(uint64_t n, uint64_t a, uint64_t b) {
    if (n == 0) {
        return a;
    }
    return fib_aux(n - 1, b, a + b);
}

static uint64_t fib(uint64_t n) {
    return fib_aux(n, 0, 1);
}

int main(void) {
    uint64_t sum = 0;
    const uint64_t repeats = 100000;

    for (uint64_t i = 0; i < repeats; ++i) {
        sum += fib(32 + (i % 2));
    }

    printf("%llu\n", (unsigned long long)sum);
    return 0;
}
