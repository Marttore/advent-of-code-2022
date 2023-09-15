using JuMP
using Cbc
#using Revise

lines = split(strip(read("day16.in", String)), "\n")

valves = Dict()
L = []
dict_input = Dict()
for line in lines
    flow = parse(Int, match(r"\d+", line).match)
    valve, conn... = [String(m.match) for m in eachmatch(r"[A-Z]{2}+", line)]
    valves[valve] = flow
    push!(L, valve)
    dict_input[valve] = conn
end

start = findfirst(isequal("AA"), L)
model = Model()
set_optimizer(model, Cbc.Optimizer)

T = 26
@variable(model, x[1:T, 1:length(L), 1:length(L)],Bin)
@variable(model, elefant[1:T, 1:length(L), 1:length(L)],Bin)
@variable(model, y[1:T,1:length(L)], Bin)

# Place entities at start
@constraint(model,sum(x[1,start,j] for j = 1:length(L)) == 1)
@constraint(model,sum(elefant[1,start,j] for j = 1:length(L)) == 1)

for t = 1:T
    for (ii, i) in enumerate(L)
        for (jj, j) in enumerate(L)
            if !(j in dict_input[i])
                if i != j
                    @constraint(model, x[t,ii,jj] == 0 )
                    @constraint(model, elefant[t,ii,jj] == 0 )
                end
            end
        end
    end
end

for t = 1:T-1
    for j = 1:length(L)
        @constraint(model,sum(x[t,i,j] for i = 1:length(L)) == sum(x[t+1,j,k] for k = 1:length(L)))
        @constraint(model,sum(elefant[t,i,j] for i = 1:length(L)) == sum(elefant[t+1,j,k] for k = 1:length(L)))
    end
end

for t = 1:T
    for i = 1:length(L)
        @constraint(model,x[t,i,i] + elefant[t,i,i] == y[t,i])
        #@constraint(model,elefant[t,i,i] == y[t,i])
    end 
end

for i = 1:length(L)
    @constraint(model, sum(y[t,i] for t = 1:T) <= 1)
end

for t = 1:T
    @constraint(model,sum(x[t,i,j] for i = 1:length(L), j=1:length(L)) <= 1)
    @constraint(model,sum(elefant[t,i,j] for i = 1:length(L), j=1:length(L)) <= 1)
end

for i = 1:length(L)
    @constraint(model,sum(y[t,i] for t= 1:T) <= 1)
end

#ingen er skrudd på ved start
for i = 1:length(L)
    @constraint(model, y[1, i] == 0)
end

obj = JuMP.AffExpr()

for t=1:T
    for (i, l) in enumerate(L)
        global obj += y[t, i] * valves[l] * (T - t)
    end
end

@objective(model, Max, obj)
res = optimize!(model) 

solution_summary(model)

println("Turning on")

for t=1:T
    for i = 1:length(L)
        if(value(y[t,i]) > 0)
            println(t, " ", L[i], "\t",  value(y[t,i]))
        end
    end
end

println("Human path")

for t=1:T
    for i = 1:length(L)
        for j = 1:length(L)
            if(value(x[t,i,j]) > 0)
                println(t, " ", L[i], " ", L[j], "\t",  value(x[t,i,j]))
            end
        end
    end
end

println("elefant path")


for t=1:26
    for i = 1:length(L)
        for j = 1:length(L)

        if(value(elefant[t,i,j]) > 0)
            println(t, " ", L[i], " ", L[j], "\t",  value(elefant[t,i,j]))
        end
    end
    end
end
