#include <cstdint>
#include <iostream>

static std::uint64_t fib(std::uint64_t n) {
    if (n <= 1) {
        return n;
    }
    return fib(n - 1) + fib(n - 2);
}

int main() {
    std::cout << fib(32) << "\n";
    return 0;
}
