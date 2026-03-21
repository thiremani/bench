let sum = 0.0;
const n = 10_000_001;

for (let i = 1; i < n; i += 1) {
    sum += 1.0 / i;
}

console.log(sum.toFixed(6));
