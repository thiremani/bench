local function fib_aux(n, a, b)
    if n == 0 then
        return a
    end
    return fib_aux(n - 1, b, a + b)
end

local function fib(n)
    return fib_aux(n, 0, 1)
end

local sum = 0
local repeats = 1000000

for i = 0, repeats - 1 do
    sum = sum + fib(32 + (i % 2))
end

io.write(string.format("%.0f\n", sum))
