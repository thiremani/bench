const std = @import("std");

pub fn main() !void {
    var stdout_buffer: [1024]u8 = undefined;
    var stdout_writer = std.fs.File.stdout().writer(&stdout_buffer);
    var sum: f64 = 0.0;
    const n: u64 = 10_000_001;
    var i: u64 = 1;

    while (i < n) : (i += 1) {
        sum += 1.0 / @as(f64, @floatFromInt(i));
    }

    try stdout_writer.interface.print("{d:.6}\n", .{sum});
    try stdout_writer.interface.flush();
}
