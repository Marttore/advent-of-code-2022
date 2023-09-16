import os
from itertools import zip_longest
from functools import cmp_to_key
from math import prod
from ast import literal_eval

day = os.path.basename(os.getcwd())

def in_right_order(pair):
    left, right = pair[0], pair[1]

    for l, r in zip_longest(left, right, fillvalue=None):
        match (l, r):
            case (None, _):
                return True
            case (_, None):
                return False
            case ([*ls], [*rs]):
                if (result := in_right_order([ls, rs])) is not None:
                    return result
            case (l, [*rs]):
                if (result := in_right_order([[l], rs])) is not None:
                    return result
            case ([*ls], r):
                if (result := in_right_order([ls, [r]])) is not None:
                    return result
            case (l, r):
                if l > r:
                    return False
                elif l < r:
                    return True

    return True

pairs = [[literal_eval(x) for x in pair.strip().split("\n")] for pair in open(f"{day}.in").read().split("\n\n")]

part_1 = sum(i + 1 for i, pair in enumerate(pairs) if in_right_order(pair))

lines = [literal_eval(x.strip()) for x in open(f"{day}.in").read().splitlines() if x]
lines.extend([[[2]], [[6]]])
less_than = lambda x, y : -1 if in_right_order((x, y)) else 1
lines = sorted(lines, key=cmp_to_key(less_than))

part_2 = prod(i+1 for i, line in enumerate(lines) if line==[[2]] or line==[[6]])

print(f"Part 1: {part_1}")
print(f"Part 2: {part_2}")
