const std = @import("std");

fn fibAux(n: u64, a: u64, b: u64) u64 {
    if (n == 0) {
        return a;
    }
    return fibAux(n - 1, b, a + b);
}

fn fib(n: u64) u64 {
    return fibAux(n, 0, 1);
}

pub fn main() !void {
    const stdout = std.fs.File.stdout().deprecatedWriter();
    try stdout.print("{}\n", .{fib(32)});
}
