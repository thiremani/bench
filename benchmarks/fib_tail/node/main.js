function fibAux(n, a, b) {
    if (n === 0) {
        return a;
    }
    return fibAux(n - 1, b, a + b);
}

function fib(n) {
    return fibAux(n, 0, 1);
}

let sum = 0;
const repeats = 100_000;

for (let i = 0; i < repeats; i += 1) {
    sum += fib(32 + (i % 2));
}

console.log(sum);
