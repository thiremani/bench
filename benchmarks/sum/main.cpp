#include <cstdint>
#include <iostream>

int main() {
    std::uint64_t sum = 0;
    const std::uint64_t n = 100000000;

    for (std::uint64_t i = 1; i <= n; ++i) {
        sum += i;
    }

    std::cout << sum << "\n";
    return 0;
}
