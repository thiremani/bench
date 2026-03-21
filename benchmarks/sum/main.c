#include <stdint.h>
#include <stdio.h>

int main(void) {
    uint64_t sum = 0;
    const uint64_t n = 100000000;

    for (uint64_t i = 1; i <= n; ++i) {
        sum += i;
    }

    printf("%llu\n", (unsigned long long)sum);
    return 0;
}
