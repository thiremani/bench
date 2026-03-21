function fib(n) {
    if (n <= 1) {
        return n;
    }
    return fib(n - 1) + fib(n - 2);
}

function benchOutput() {
    return String(fib(32));
}

if (typeof require !== "undefined" && require.main === module) {
    console.log(benchOutput());
}

module.exports = { benchOutput };
