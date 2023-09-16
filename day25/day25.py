import os
from math import log

day = os.path.basename(os.getcwd())

def snafu_decoder(number):
    num = 0
    for pos, char in enumerate(number.strip()[::-1]):
        match char:
            case "=":
                num += -2 * 5**pos
            case "-":
                num += -1 * 5**pos
            case str():
                num += int(char) * 5**pos
    return num

part_1 = 0
for row in open(f"{day}.in"):
    num = snafu_decoder(row)
    part_1 += num

length = int(log(part_1, 5))
out = ["0"] * (length + 1)

for i in range(length,-1,-1):
    idx = length - i 
    multi = part_1 / 5**i
    if multi > 1.5:
        part_1 = part_1 - 2 * 5**i
        out[idx] = "2"
    elif multi > 0.5:
        part_1 = part_1 - 1 * 5**i
        out[idx] = "1"
    elif multi > -0.5:
        out[idx] = "0"
    elif multi > -1.5:
        part_1 = part_1 + 1 * 5**i
        out[idx] = "-"
    else:
        part_1 = part_1 + 2 * 5**i
        out[idx] = "="

print(f"Part 1: {''.join(out)}")
