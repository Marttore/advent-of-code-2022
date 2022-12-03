lines = open("day03.in").read().splitlines()

def calc_prio(c) :
    if c.isupper():
        return ord(c) - ord("A") + 27
    else:
        return ord(c) - ord("a") + 1

part_1 = 0
for line in lines:
    middle = len(line) // 2
    first, second = set(line[:middle]), set(line[middle:])

    inter  = first & second
    part_1 += calc_prio(inter.pop())

part_2 = 0
for i in range(0, len(lines), 3):
    first  = set(lines[i])
    second = set(lines[i + 1])
    third  = set(lines[i + 2])
         
    inter  = first & second & third 
    part_2 += calc_prio(inter.pop())


print(f"Part 1: {part_1}")
print(f"Part 2: {part_2}")
