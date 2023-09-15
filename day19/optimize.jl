using JuMP
using Cbc

N = 4

function get_optimum_geode(blueprint_string, T)
    id, digits... = [parse(Int, m.match) for m in eachmatch(r"\d+", blueprint_string)]

    cost = Dict(
        1 => [digits[1],         0,         0, 0],
        2 => [digits[2],         0,         0, 0],
        3 => [digits[3], digits[4],         0, 0],
        4 => [digits[5],         0, digits[6], 0],
    )

    model = Model(Cbc.Optimizer)
    set_silent(model)

    @variable(model, minerals[1:T, 1:4] >= 0, integer=true)
    @variable(model, robots[1:T, 1:4] >= 0, integer=true)
    @variable(model, build[1:T, 1:4] >= 0, Bin)

    for n in 1:N
        @constraint(model, robots[1, n] == (n==1 ? 1 : 0))
        @constraint(model, minerals[1, n] == (n==1 ? 1 : 0) )
        @constraint(model, build[1, n] == 0 )
    end

    for t = 2:T
        @constraint(model, sum(build[t, n] for n in 1:N) <= 1)
        for n in 1:N
            @constraint(model, robots[t, n] == robots[t - 1, n] + build[t - 1, n])
            @constraint(model, minerals[t, n] == minerals[t - 1, n] + robots[t - 1, n] - sum(build[t, j] * cost[j][n] for j in 1:N))
        end
    end

    @objective(model, Max, minerals[T, 4])
    res = optimize!(model)
    #println("Optimum: ", objective_value(model))
    return objective_value(model)
end

blueprints = read("day19.in", String) |> strip |> f -> split(f,"\n")
part_1 = round(Int, sum(get_optimum_geode(bp, 24) * i for (i, bp) in enumerate(blueprints)))
part_2 = round(Int, prod(get_optimum_geode(bp, 32) for bp in blueprints[1:3]))

println("Part 1: $(part_1)")
println("Part 2: $(part_2)")

# for t=1:T   
#     println(t, " minerals", "\t", int.(value.(minerals[t, :])))
#     println(t, " rob", "\t", int.(value.(robots[t, :])))
#     println(t, " buy", "\t", int.(value.(buying[t, :])))
#     println()
# end
