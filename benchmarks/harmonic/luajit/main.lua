local sum = 0.0
local n = 10000001

for i = 1, n - 1 do
    sum = sum + 1.0 / i
end

io.write(string.format("%.6f\n", sum))
