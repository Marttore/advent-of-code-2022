import os
from collections import deque

day = os.path.basename(os.getcwd())

cubes = set(tuple(map(int, x.split(","))) for x in open(f"{day}.in").read().splitlines())

sides = [
        (0, 0, 1),
        (0, 0, -1),
        (1, 0, 0),
        (-1, 0, 0),
        (0, 1, 0),
        (0, -1, 0)
        ]

t = 0
for cube in cubes:
    for side in sides:
        adj = cube[0] + side[0], cube[1] + side[1], cube[2] + side[2]
        if adj not in cubes:
             t += 1

Q = deque()
Q.append((0, 0 , 0 ))
seen = set()

part_2 = 0
while Q:
    point = Q.popleft()
    for side in sides:
        adj = point[0] + side[0], point[1] + side[1], point[2] + side[2]
        if adj not in seen:
            if adj in cubes:
                part_2 += 1
            elif -4 < adj[0] < 24 and -4 < adj[1] < 24 and -4 < adj[2] < 24:
                Q.append(adj)
                seen.add(adj)

part_1 = t



print(f"Part 1: {part_1}")
print(f"Part 2: {part_2}")
