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
    var stdout_buffer: [1024]u8 = undefined;
    var stdout_writer = std.fs.File.stdout().writer(&stdout_buffer);
    try stdout_writer.interface.print("{}\n", .{fib(32)});
    try stdout_writer.interface.flush();
}
