import os
from copy import deepcopy
day = os.path.basename(os.getcwd())

jets = open(f"{day}.in").read().strip()

min_col = 0
max_col = 7

line = (0 + 0j, 0 + 1j, 0 + 2j, 0 + 3j)
cross = (0 + 1j, 1 + 0j, 1 + 1j, 1 + 2j, 2 + 1j)
L = (2 + 2j, 1 + 2j, 0 + 0j, 0 + 1j, 0 + 2j)
I = (0 + 0j, 1 + 0j, 2 + 0j, 3 + 0j)
square = (0 + 0j, 0 + 1j, 1 + 0j, 1 + 1j)

shapes = [line, cross, L, I, square]

def top_spawn(grid):
    return max(p.real for p in grid) + 4 if grid else 4

def add_to_rock(rock, complex_number):
    for i in range(len(rock)):
        rock[i] += complex_number
    return rock

def show_grid(grid, rock=None):
    height = int(max(p.real for p in grid)) + 4 if grid else 4
    for r in range(height, 0, -1):
        print("|", end="")
        for c in range(7):
            if r + c *1j in grid:
                print("#", end="")
            elif rock is not None and r + c *1j in rock:
                print("@", end="")
            else:
                print(".", end="")
        print("|", end="")
        print()
    print("+--------+")
    print()

left = 2
top = 4

dropped_rocks = 0
grid = set()

current_jet = 0

prev_jet = 0
prev_rock = 0
prev_h = 0
while dropped_rocks < 5_000_000:
    if dropped_rocks % 1710 == 1090:
        h = int(top_spawn(grid) - 4)
        print(current_jet, dropped_rocks, h, current_jet-prev_jet, dropped_rocks - prev_rock, h - prev_h)
        prev_jet = current_jet
        prev_rock = dropped_rocks
        prev_h = h
        #if dropped_rocks % len(shapes) == 0:
            #print("yo", dropped_rocks)
    rock = list(deepcopy(shapes[dropped_rocks % len(shapes)]))

    #top = top_spawn(grid)

    rock = add_to_rock(rock, top + left*1j)



    stopped = False

    while not stopped:
        #show_grid(grid, rock)
        jet = jets[current_jet % len(jets)]
        current_jet += 1
        dir = 1j if jet == ">" else -1j

        rows = set(x.real for x in rock)
        side_blocked = False
        for row in rows:

            if jet == ">":
                col = max(x.imag for x in rock if x.real == row)
            else:
                col = min(x.imag for x in rock if x.real == row)

            edge = row + (col * 1j) + dir
            if edge.imag < 0 or edge.imag > 6 or edge in grid:
                side_blocked = True

        if not side_blocked:
            rock = add_to_rock(rock, dir)




        cols = set(x.imag for x in rock)

        for col in cols:
            row = min(x.real for x in rock if x.imag == col)
            under = row - 1 + col * 1j
            if under.real == 0 or under in grid:
                stopped = True

        if not stopped:
            rock = add_to_rock(rock, -1)
    
    for point in rock:
        assert point not in grid
        if point.real + 4 > top:
            top = point.real + 4
        grid.add(point)

    dropped_rocks += 1
    if dropped_rocks % 100_000 == 0:
        print(dropped_rocks)

    #if dropped_rocks == 7:
    #    show_grid(grid)

   #     break
    




part_1 = int(top_spawn(grid) - 4)
part_2 = 0


print(f"Part 1: {part_1}")
print(f"Part 2: {part_2}")
