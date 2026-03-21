#include <iostream>
#include <cstdint>
#include <iomanip>

int main() {
    double sum = 0.0;
    const std::uint64_t n = 10000001;

    for (std::uint64_t i = 1; i < n; ++i) {
        sum += 1.0 / (double)i;
    }

    std::cout << std::fixed << std::setprecision(6) << sum << "\n";
    return 0;
}
