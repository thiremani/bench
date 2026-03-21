fn main() {
    let mut sum: u64 = 0;
    let n: u64 = 100_000_000;

    for i in 1..=n {
        sum += i;
    }

    println!("{}", sum);
}
