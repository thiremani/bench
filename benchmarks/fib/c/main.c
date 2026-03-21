#include <stdint.h>
#include <stdio.h>

static uint64_t fib(uint64_t n) {
    if (n <= 1) {
        return n;
    }
    return fib(n - 1) + fib(n - 2);
}

int main(void) {
    printf("%llu\n", (unsigned long long)fib(32));
    return 0;
}
