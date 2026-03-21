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
    let mut sum: u64 = 0;
    let repeats: u64 = 1_000_000;

    for i in 0..repeats {
        sum += fib(32 + (i % 2));
    }

    println!("{}", sum);
}
