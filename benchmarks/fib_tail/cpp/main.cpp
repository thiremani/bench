#include <cstdint>
#include <iostream>

static std::uint64_t fib_aux(std::uint64_t n, std::uint64_t a, std::uint64_t b) {
    if (n == 0) {
        return a;
    }
    return fib_aux(n - 1, b, a + b);
}

static std::uint64_t fib(std::uint64_t n) {
    return fib_aux(n, 0, 1);
}

int main() {
    std::uint64_t sum = 0;
    const std::uint64_t repeats = 1000000;

    for (std::uint64_t i = 0; i < repeats; ++i) {
        sum += fib(32 + (i % 2));
    }

    std::cout << sum << "\n";
    return 0;
}
