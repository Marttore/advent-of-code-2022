with open("day1.in") as f:
    calories = [[int(x) for x in l.strip().split("\n")] for l in f.read().split("\n\n")]

summed_cals = list(map(sum, calories))

print(f"Part 1: {max(summed_cals)}")

max3 = sum(sorted(summed_cals, reverse=True)[0:3])

print(f"Part 2: {max3}")
