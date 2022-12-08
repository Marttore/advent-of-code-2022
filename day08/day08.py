import os

day = os.path.basename(os.getcwd())

trees = open(f"{day}.in").read().splitlines()
trees = [[int(x) for x in row] for row in trees]

height = len(trees)
width = len(trees[0])

deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def inbounds(x, y):
    return 0 <= x < height  and 0 <= y < width

sum_visible = 0
for x in range(1, height-1):
    for y in range(1, width-1):

        this_tree = trees[x][y]
        for dx, dy in deltas:
            i, j = x + dx, y + dy

            visible = True
            while(inbounds(i, j)):
                if trees[i][j] >= this_tree: 
                    visible = False
                    break
                i, j = i + dx, j + dy

            if visible:
                sum_visible += 1
                break


max_scenicscore = 1
for x in range(0, height-1):
    for y in range(0, width-1):
        this_tree = trees[x][y]
        sc = 1
        for dx, dy in deltas:
            dist = 0
            i, j = x + dx, y + dy
            while(inbounds(i, j)):
                dist += 1
                if trees[i][j] >= this_tree: break
                i, j = i + dx, j + dy
            sc *= dist

        if sc > max_scenicscore:
            max_scenicscore = sc

part_1 = sum_visible + 2*width + 2*(height-2)
part_2 = max_scenicscore


print(f"Part 1: {part_1}")
print(f"Part 2: {part_2}")
