function fibAux(n, a, b) {
    if (n === 0) {
        return a;
    }
    return fibAux(n - 1, b, a + b);
}

function fib(n) {
    return fibAux(n, 0, 1);
}

console.log(fib(32));
