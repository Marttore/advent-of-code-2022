import os
day = os.path.basename(os.getcwd())

mat = [[x for x in line] for line in open(f"{day}.in").read().splitlines()]

rows = len(mat)
cols = len(mat[0])

prev = { (row, col) : None for col in range(cols) for row in range(rows)}
dist = { (row, col) : 10000 for col in range(cols) for row in range(rows)}

end = [(r, c) for c in range(cols) for r in range(rows) if mat[r][c] == 'E'][0]
start = [(r, c) for c in range(cols) for r in range(rows) if mat[r][c] == 'S'][0]

visited = set(end)
dist[end] =  0
q = [end]

def conv_val(ch):
    if ch == "S":
        ch = "a"
    if ch == "E":
        ch = "z"
    return ch

while q:
    row, col = q.pop(0)

    val = conv_val(mat[row][col])
    visited.update([(row, col)])

    for i, j  in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
        ir = row + i
        ic = col + j

        if 0 <= ir < rows and 0 <= ic < cols:
            if ord(val) - ord(conv_val(mat[ir][ic])) <= 1 and (ir, ic) not in visited:
                alt = dist[(row, col)] + 1
                if alt < dist[(ir, ic)]:
                    dist[(ir, ic)] = alt
                    prev[(ir, ic)] = (row, col)
                    q.append((ir,ic))



p=start
visited = set([start, end])
while p != end:
    p = prev[p]
    visited.update([p])

for r in range(rows):
    for c in range(cols):
        if (r, c) in visited:
            print("\x1b[6;30;42m" + mat[r][c] + '\x1b[0m', end="")
        else:
            print(mat[r][c], end="")

    print()

part_1 = dist[start]
part_2 = sorted(dist[p] for p in dist if mat[p[0]][p[1]] in "Sa")[0]

print(f"Part 1: {part_1}")
print(f"Part 2: {part_2}")
