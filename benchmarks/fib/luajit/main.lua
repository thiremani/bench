local function fib(n)
    if n <= 1 then
        return n
    end
    return fib(n - 1) + fib(n - 2)
end

io.write(string.format("%.0f\n", fib(32)))
