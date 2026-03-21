function benchOutput() {
    let sum = 0.0;
    const n = 10_000_001;

    for (let i = 1; i < n; i += 1) {
        sum += 1.0 / i;
    }

    return sum.toFixed(6);
}

if (typeof require !== "undefined" && require.main === module) {
    console.log(benchOutput());
}

module.exports = { benchOutput };
