import os
from math import lcm
from collections import deque


day = os.path.basename(os.getcwd())

lines = open(f"{day}.in").read().splitlines()

w, h = len(lines[0]) - 2, len(lines) - 2
dirs = (1, 1j, 0, -1, -1j)

blizz_dir = {">": 1j, "<": -1j, "^": -1, "v": 1}
blizzards = []
for row, line in enumerate(lines[1:-1]):
    for col, char in enumerate(line[1:-1]):
        if char != ".":
            blizzards.append((row + col * 1j, blizz_dir[char]))


cycle_length = lcm(w, h)
blizzard_cycle = []

for i in range(cycle_length):
    blizzard_cycle.append(set())
    for blizz_pos, dir in blizzards:
        new_pos = blizz_pos + dir * i
        new_pos = complex(new_pos.real % h, new_pos.imag % w)
        blizzard_cycle[i].add(new_pos)


def bfs(start, goal, time):
    Q = deque()
    Q.append((start, time, []))
    visited = set()
    while Q:
        pos, time, path = Q.popleft()

        for dir in dirs:
            new = pos + dir
            if new == goal:
                path.append(pos)
                path.append(goal)
                return time + 1, path

            if new not in blizzard_cycle[(time + 1) % cycle_length]:
                if (0 <= new.real < h and 0 <= new.imag < w) or new == start:
                    new_state = (new, time + 1)
                    if new_state not in visited:
                        visited.add(new_state)
                        new_state = (new, time + 1, path + [pos])
                        Q.append(new_state)


START = -1
END = complex(h, w - 1)
part_1, path = bfs(START, END, 0)
middle, _ = bfs(END, START, part_1)
part_2, _ = bfs(START, END, middle)

print(f"Part 1: {part_1}")
print(f"Part 2: {part_2}")
