function benchOutput() {
    let sum = 0;
    const n = 20_000_000;

    for (let i = 1; i <= n; i += 1) {
        sum += (i * 3) % 17;
    }

    return String(sum);
}

if (typeof require !== "undefined" && require.main === module) {
    console.log(benchOutput());
}

module.exports = { benchOutput };
