#include <cstdint>
#include <cstdio>

int main() {
    double sum = 0.0;
    const std::uint64_t n = 10000001;

    for (std::uint64_t i = 1; i < n; ++i) {
        sum += 1.0 / (double)i;
    }

    std::printf("%.6f\n", sum);
    return 0;
}
