fn fib_aux(n: u64, a: u64, b: u64) -> u64 {
    if n == 0 {
        return a;
    }
    fib_aux(n - 1, b, a + b)
}

fn fib(n: u64) -> u64 {
    fib_aux(n, 0, 1)
}

fn main() {
    println!("{}", fib(32));
}
