local sum = 0
local n = 20000000

for i = 1, n do
    sum = sum + ((i * 3) % 17)
end

io.write(string.format("%.0f\n", sum))
