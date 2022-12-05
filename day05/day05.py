import os
import re

day = os.path.basename(os.getcwd())

header, moves = open(f"{day}.in").read().split("\n\n")
moves = moves.strip().split("\n")

def parse_header(header):
    header_lines = header.split("\n")

    n_columns = int(header_lines[-1].split()[-1])

    stacks = [[] for _ in range(n_columns)]

    for line in header_lines[-2::-1]:
        for col in range(n_columns):
            content = line[4*col+1:4*col+2]
            if content != " ":
                stacks[col].append(content)

   
    return stacks

stacks_1 = parse_header(header)
stacks_2 = parse_header(header)

def parse_move(move):
    digits = re.findall(r"move (\d+) from (\d+) to (\d+)", move)
    return tuple(int(x) for x in digits[0])


def part_1(stacks, moves):
    for move in moves:
        count, frm, to = parse_move(move)

        for _ in range(count):
            tmp = stacks[frm - 1].pop(-1)
            stacks[to - 1].append(tmp)

    return "".join([st[-1] for st in stacks])


def part_2(stacks, moves):
    for move in moves:
        count, frm, to = parse_move(move)

        tmp_list = []
        for _ in range(count):
            if len(stacks[frm - 1]) > 0:
                tmp = stacks[frm - 1].pop(-1)
                tmp_list.insert(0, tmp)

        stacks[to - 1].extend(tmp_list)

    return "".join([st[-1] for st in stacks])

part_1 = part_1(stacks_1, moves)
part_2 = part_2(stacks_2, moves)


print(f"Part 1: {part_1}")
print(f"Part 2: {part_2}")
