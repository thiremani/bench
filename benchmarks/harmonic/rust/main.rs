fn main() {
    let mut sum: f64 = 0.0;
    let n: u64 = 10_000_001;

    for i in 1..n {
        sum += 1.0 / (i as f64);
    }

    println!("{:.6}", sum);
}
