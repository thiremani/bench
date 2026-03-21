const std = @import("std");

fn fib(n: u64) u64 {
    if (n <= 1) {
        return n;
    }
    return fib(n - 1) + fib(n - 2);
}

pub fn main() !void {
    const stdout = std.fs.File.stdout().deprecatedWriter();
    try stdout.print("{}\n", .{fib(32)});
}
