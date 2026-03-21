#include <stdio.h>
#include <stdint.h>

int main(void) {
    double sum = 0.0;
    const uint64_t n = 10000001;

    for (uint64_t i = 1; i < n; ++i) {
        sum += 1.0 / (double)i;
    }

    printf("%.6f\n", sum);
    return 0;
}
