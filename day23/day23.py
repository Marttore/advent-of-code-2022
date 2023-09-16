import os
import re
from collections import Counter

day = os.path.basename(os.getcwd())

elves = {
    (r + c * 1j) 
    for r, row in enumerate(open(f"{day}.in").read().splitlines())
    for c, char in enumerate(row)
    if char == "#"
}

moves = [
    (-1, [-1, -1 + 1j, -1 - 1j]),
    (1, [1, 1 + 1j, 1 - 1j]),
    (-1j, [-1j, -1 - 1j, 1 - 1j]),
    (1j, [1j, -1 + 1j, 1 + 1j]),
]
all_dirs = set(x for m in moves for x in m[1])

round = 1
while True:
    potential_moves = {}
    for elf in elves:
        if any(elf + dir in elves for dir in all_dirs):
            for l in range(4):
                dir, considerations = moves[((round - 1) + l) % 4]
                if all(elf + c not in elves for c in considerations):
                    potential_moves[elf] = elf+ dir
                    break
                    
    cntr = Counter(potential_moves.values())
    
    moved = False
    for (frm, to) in potential_moves.items():
        if cntr[to] == 1:
            moved = True
            elves.add(to)
            elves.remove(frm)
    
    if moved == False:
        part_2 = round
        break
    
    if round == 10:
        minr = int(min(x.real for x in elves))
        maxr = int(max(x.real for x in elves))
        minc = int(min(x.imag for x in elves))
        maxc = int(max(x.imag for x in elves))

        part_1 = 0
        for i in range(minr, maxr + 1):
            for j in range(minc, maxc + 1):
                if (i + j * 1j) not in elves:
                    part_1 += 1

    round += 1

    
print(f"Part 1: {part_1}")
print(f"Part 2: {part_2}")