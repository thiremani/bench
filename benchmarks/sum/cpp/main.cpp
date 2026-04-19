#include <cstdint>
#include <cstdio>

int main() {
    std::uint64_t sum = 0;
    const std::uint64_t n = 20000000;

    for (std::uint64_t i = 1; i <= n; ++i) {
        sum += (i * 3) % 17;
    }

    std::printf("%llu\n", static_cast<unsigned long long>(sum));
    return 0;
}
