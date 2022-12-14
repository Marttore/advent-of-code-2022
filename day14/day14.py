import os
from copy import deepcopy

day = os.path.basename(os.getcwd())

paths = [[tuple(map(int, point.strip().split(","))) for point in path.split(" -> ")] for path in open(f"{day}.in").readlines()]
SAND_START = (500, 0)

def parse_path(path, grid):
    prev = path[0]
    for p in path[1:]:
        if p[0] != prev[0]:
            x_dir = 1 if p[0] >= prev[0] else -1
            for x in range(prev[0], p[0] + x_dir , x_dir):
                grid[(x, prev[1])] = "#"
        else:
            y_dir = 1 if p[1] >= prev[1] else -1
            for y in range(prev[1], p[1] + y_dir, y_dir):
                grid[(prev[0], y)] = "#"
        prev = p


def drop_sand(grid, ymax, infinite):
    point = SAND_START

    if SAND_START in grid:
        return - 1 

    while True:
        if infinite and point[1] > ymax: 
                return -1
        elif not infinite and point[1] + 1 == ymax: 
                grid[point] = "o"
                return 1
        elif (point[0], point[1] + 1) not in grid:
            point = (point[0], point[1] + 1)
        elif (point[0] - 1 , point[1] + 1) not in grid:
            point = (point[0] - 1, point[1] + 1)
        elif (point[0] + 1 , point[1] + 1) not in grid:
            point = (point[0] + 1, point[1] + 1)
        else:
            grid[point] = "o"
            return 1


def print_grid(grid):
    ymin = 0
    ymaxx = max(grid.keys(), key=lambda x: x[1])[1]
    xmin = min(grid.keys(), key=lambda x: x[0])[0]
    xmax = max(grid.keys(), key=lambda x: x[0])[0]

    file = open("sand.txt", "w")
    for y in range(ymin - 1, ymaxx + 2):
        for x in range(xmin - 1, xmax + 2):
            if (x, y) == SAND_START:
                if (x, y) in grid and  grid[x, y] == "o":
                    print("o", end="", file=file)
                else:
                    print("+", end="", file=file)
            elif y == ymax:
                print("#", end="", file=file)
            elif (x, y) not in grid:
                print(".", end="", file=file)
            elif grid[x, y] == "#":
                print("#", end="", file=file)
            elif grid[x, y] == "o":
                print("o", end="", file=file)
        print(file=file)


grid = {}
for path in paths:
    parse_path(path, grid)
grid2 = deepcopy(grid)

ymax = max(grid2.keys(), key=lambda x: x[1])[1] + 2

while drop_sand(grid, ymax, infinite=True) != -1:
    continue

while drop_sand(grid2, ymax, infinite=False) != -1:
    continue

part_1 = sum(1 for v in grid.values() if v == "o")
part_2 = sum(1 for v in grid2.values() if v == "o")
print_grid(grid2)

print(f"Part 1: {part_1}")
print(f"Part 2: {part_2}")
