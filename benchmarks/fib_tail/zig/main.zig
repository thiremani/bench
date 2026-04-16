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

pub fn main(init: std.process.Init) !void {
    const io = init.io;
    var stdout_buffer: [1024]u8 = undefined;
    var stdout_writer = std.Io.File.stdout().writer(io, &stdout_buffer);
    const stdout = &stdout_writer.interface;
    var sum: u64 = 0;
    const repeats: u64 = 1_000_000;
    var i: u64 = 0;

    while (i < repeats) : (i += 1) {
        sum += fib(32 + (i % 2));
    }

    try stdout.print("{}\n", .{sum});
    try stdout.flush();
}
