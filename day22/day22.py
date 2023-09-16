import os
import re


day = os.path.basename(os.getcwd())
raw_grid, path =  open(f"{day}.in").read().split("\n\n")
path = path.strip()

grid = {} 
cube_side = {}
for r, text in enumerate(raw_grid.splitlines()):
    for c, char in enumerate(text):
        if char == "." or char=="#":
            grid[(r + 1) + (c + 1) * 1j] = char
            
            if r < 50:
                if c < 100:
                    cube_side[(r + 1) + (c + 1) * 1j] = 1
                else:
                    cube_side[(r + 1) + (c + 1) * 1j] = 2
            elif r < 100:
                    cube_side[(r + 1) + (c + 1) * 1j] = 3
            elif r < 150:
                if c < 50:
                    cube_side[(r + 1) + (c + 1) * 1j] = 4
                else:
                    cube_side[(r + 1) + (c + 1) * 1j] = 5
            else:
                cube_side[(r + 1) + (c + 1) * 1j] = 6

side_cube = { 1 : [], 2 : [], 3 : [], 4 : [], 5 : [], 6 : [] }

for point, cube in cube_side.items():
    side_cube[cube].append(point)


cube_conn = {
        1: {
            1 : (3, 1),
            -1 : (6, 1j),
            1j : (2, 1j),
            -1j : (4, 1j),
            },
        2: {
            1 : (3, -1j),
            -1 : (6, -1),
            1j : (5, -1j),
            -1j : (1, -1j),
            },
        3: {
            1 : (5, 1),
            -1 : (1, -1),
            1j : (2, -1),
            -1j :(4, 1),
            },
        4: {
            1 : (6, 1),
            -1 : (3, 1j),
            1j : (5, 1j),
            -1j : (1, 1j),
            },
        5: {
            1 : (6, -1j),
            -1 : (3, -1),
            1j : (2, -1j),
            -1j : (4, -1j),
            },
        6: {
            1 : (2, 1),
            -1 : (4, -1),
            1j : (5, -1),
            -1j : (1, 1),
            },
}


def get_path_elements(path):
    for e in re.findall(r"\d+|[A-Z]", path):
        yield e

start_c = min(x.imag for x in grid.keys() if x.real == 1)
current = 1 + start_c * 1j
dir = 1j
p = get_path_elements(path)
try:
    while (forward := next(p)):
        count  = int(forward)
        for _ in range(count):
            if current + dir not in grid:
                if dir == 1:
                    next_pos = min(x.real for x in grid if x.imag == current.imag) + current.imag * 1j 
                elif dir == -1:
                    next_pos = max(x.real for x in grid if x.imag == current.imag) + current.imag * 1j 
                elif dir == 1j:
                    next_pos =  current.real + min(x.imag for x in grid if x.real == current.real) * 1j 
                elif dir == -1j:
                    next_pos =  current.real + max(x.imag for x in grid if x.real == current.real) * 1j 
                else:
                    raise ValueError
            else:
                next_pos = current + dir

            if grid[next_pos] == "#":
                break
            elif grid[next_pos] == ".":
                current = next_pos
            else:
                print(grid[next_pos], next_pos)
                raise TypeError
            

        next_dir = next(p)
        dir = dir * -1j if next_dir == "R" else dir * 1j

except StopIteration:
    pass

    
print(current, dir)
point_dir = {1j : 0, 1:1, -1j:2, -1:3}
part_1 = 1000 * current.real + 4 * current.imag + point_dir[dir]

current = 1 + start_c * 1j
dir = 1j
p = get_path_elements(path)
try:
    while (forward := next(p)):
        count  = int(forward)
        for _ in range(count):
            if current + dir not in grid:
                next_cube, next_dir = cube_conn[cube_side[current]][dir]
                if dir == 1:
                    side = 49 - ((current.imag-1) % 50)
                elif dir == -1:
                    side = (current.imag-1) % 50
                elif dir == 1j:
                    side = (current.real-1) % 50
                elif dir == -1j:
                    side = 49 - ((current.real-1) % 50)

                next_points = side_cube[next_cube]
                if next_dir == 1:
                    next_r = min(x.real for x in next_points)
                    next_c = min(x.imag for x in next_points) + (49 - side)
                elif next_dir == -1:
                    next_r = max(x.real for x in next_points)
                    next_c = min(x.imag for x in next_points) + side
                elif next_dir == 1j:
                    next_r = min(x.real for x in next_points) + side
                    next_c = min(x.imag for x in next_points)
                elif next_dir == -1j:
                    next_r = min(x.real for x in next_points) + (49 - side)
                    next_c = max(x.imag for x in next_points) 

                next_pos = next_r + next_c * 1j 

            else:
                next_pos = current + dir
                next_dir = dir

            if grid[next_pos] == "#":
                break
            elif grid[next_pos] == ".":
                current = next_pos
                dir = next_dir       

        turn = next(p)
        dir = dir * -1j if turn == "R" else dir * 1j

except StopIteration:
    pass

    
part_2 = 1000 * current.real + 4 * current.imag + point_dir[dir]


print(f"Part 1: {int(part_1)}")
print(f"Part 2: {int(part_2)}")
