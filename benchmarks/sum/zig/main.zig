const std = @import("std");

pub fn main(init: std.process.Init) !void {
    const io = init.io;
    var stdout_buffer: [1024]u8 = undefined;
    var stdout_writer = std.Io.File.stdout().writer(io, &stdout_buffer);
    const stdout = &stdout_writer.interface;
    var sum: u64 = 0;
    const n: u64 = 20_000_000;
    var i: u64 = 1;

    while (i <= n) : (i += 1) {
        sum += (i * 3) % 17;
    }

    try stdout.print("{}\n", .{sum});
    try stdout.flush();
}
