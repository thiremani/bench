#!/usr/bin/env node

const path = require("path");
const readline = require("readline");

if (process.argv.length !== 3) {
    process.stdout.write("ERR expected source path\n");
    process.exit(1);
}

const sourcePath = path.resolve(process.argv[2]);
let benchOutput;

try {
    ({ benchOutput } = require(sourcePath));
    if (typeof benchOutput !== "function") {
        throw new Error("missing benchOutput export");
    }
} catch (err) {
    process.stdout.write(`ERR ${err.message}\n`);
    process.exit(1);
}

const rl = readline.createInterface({
    input: process.stdin,
    crlfDelay: Infinity,
});

rl.on("line", (line) => {
    const cmd = line.trim();
    if (cmd === "run") {
        try {
            process.stdout.write(`OK ${benchOutput()}\n`);
        } catch (err) {
            process.stdout.write(`ERR ${err.message}\n`);
            rl.close();
            process.exitCode = 1;
        }
    } else if (cmd === "exit") {
        rl.close();
    }
});

rl.on("close", () => {
    process.exit(process.exitCode ?? 0);
});
