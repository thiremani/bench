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
    std::cout << fib(32) << "\n";
    return 0;
}
