source_path = abspath(ARGS[1])

module BenchRuntime
end

Base.include(BenchRuntime, source_path)
bench_output = getfield(BenchRuntime, :bench_output)

for raw in eachline(stdin)
    cmd = strip(raw)
    if cmd == "run"
        try
            println("OK ", bench_output())
        catch err
            println("ERR ", sprint(showerror, err))
            flush(stdout)
            exit(1)
        end
        flush(stdout)
    elseif cmd == "exit"
        break
    end
end
