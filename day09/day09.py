import os

day = os.path.basename(os.getcwd())
moves = open(f"{day}.in").read().splitlines()


move_dir = {
    "R": (0, 1),
    "L": (0, -1),
    "U": (1, 0),
    "D": (-1, 0)
}

def is_adjacent(head, tail):
    for r in range(-1, 2):
        for c in range(-1, 2):
            if (head[0] + r, head[1] + c) == tail:
                return True
    else:
        return False


def tail_move(head, tail):
    if is_adjacent(head, tail):
        return tail

    dx, dy = head[0] - tail[0], head[1] - tail[1]

    if dx != 0 and dy != 0:
        tail = (
            tail[0] + ((dx/abs(dx)) if dx else 0),
            tail[1] + ((dy/abs(dy)) if dy else 0)
        )

    return tail


def move_rope(len_rope):
    rope = [(0, 0)] * len_rope
    tail_visited = set()
    for mv in moves:
        m = mv.split(" ")
        dir, cnt = m[0], int(m[1])

        for _ in range(cnt):
            c = move_dir[dir]
            rope[0] = rope[0][0] + c[0], rope[0][1] + c[1]
            for i in range(1, len_rope):
                rope[i] = tail_move(rope[i-1], rope[i])
            tail_visited.update([rope[-1]])

    return tail_visited


part_1 = len(move_rope(2))
part_2 = len(move_rope(10))


print(f"Part 1: {part_1}")
print(f"Part 2: {part_2}")
