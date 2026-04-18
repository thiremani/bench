const std = @import("std");

pub fn main() !void {
    const stdout = std.fs.File.stdout().deprecatedWriter();
    var sum: f64 = 0.0;
    const n: u64 = 10_000_001;
    var i: u64 = 1;

    while (i < n) : (i += 1) {
        sum += 1.0 / @as(f64, @floatFromInt(i));
    }

    try stdout.print("{d:.6}\n", .{sum});
}
