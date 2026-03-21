const std = @import("std");

pub fn main() !void {
    var stdout_buffer: [1024]u8 = undefined;
    var stdout_writer = std.fs.File.stdout().writer(&stdout_buffer);
    var sum: u64 = 0;
    const n: u64 = 100_000_000;
    var i: u64 = 1;

    while (i <= n) : (i += 1) {
        sum += i;
    }

    try stdout_writer.interface.print("{}\n", .{sum});
    try stdout_writer.interface.flush();
}
