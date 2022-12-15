elves = split(read("day1.in", String), "\n\n")

calories_per_elf = [parse.(Int, split(elf, "\n")) for elf in elves]

sum_per_elf = sum.(calories_per_elf)
top3 = partialsort(sum_per_elf, 1:3, rev=true) |> sum 

@show maximum(sum_per_elf)
@show top3;
