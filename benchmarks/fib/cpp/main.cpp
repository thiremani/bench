#include <cstdint>
#include <cstdio>

static std::uint64_t fib(std::uint64_t n) {
    if (n <= 1) {
        return n;
    }
    return fib(n - 1) + fib(n - 2);
}

int main() {
    std::printf("%llu\n", static_cast<unsigned long long>(fib(32)));
    return 0;
}
