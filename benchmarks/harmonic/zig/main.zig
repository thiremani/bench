const std = @import("std");

pub fn main(init: std.process.Init) !void {
    const io = init.io;
    var stdout_buffer: [1024]u8 = undefined;
    var stdout_writer = std.Io.File.stdout().writer(io, &stdout_buffer);
    const stdout = &stdout_writer.interface;
    var sum: f64 = 0.0;
    const n: u64 = 10_000_001;
    var i: u64 = 1;

    while (i < n) : (i += 1) {
        sum += 1.0 / @as(f64, @floatFromInt(i));
    }

    try stdout.print("{d:.6}\n", .{sum});
    try stdout.flush();
}
