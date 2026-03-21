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
    printf("%llu\n", (unsigned long long)fib(32));
    return 0;
}
