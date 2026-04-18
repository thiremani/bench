const std = @import("std");

pub fn main() !void {
    const stdout = std.fs.File.stdout().deprecatedWriter();
    var sum: u64 = 0;
    const n: u64 = 20_000_000;
    var i: u64 = 1;

    while (i <= n) : (i += 1) {
        sum += (i * 3) % 17;
    }

    try stdout.print("{}\n", .{sum});
}
