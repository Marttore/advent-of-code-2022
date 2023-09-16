import os
import re
from itertools import pairwise
from collections import defaultdict

day = os.path.basename(os.getcwd())

rows = [list(map(int, re.findall(r"[-\d]+", row))) for row in open(f"{day}.in").readlines()]

scanned = defaultdict(list)
beacons = set()

LOWER = 0
UPPER = 4000000
for i, (sensor_x, sensor_y, beacon_x, beacon_y) in enumerate(rows):
    dist = abs(beacon_x - sensor_x) + abs(beacon_y - sensor_y)
    beacons.add((beacon_x, beacon_y))
    print(i)

    for dy in range(-dist, dist + 1 ):
        row = sensor_y + dy
        if row < LOWER:
            continue
        if row > UPPER:
            break
        dx = dist - abs(dy)

        l = sensor_x - dx
        u = sensor_x + dx 

        scanned[row].append((l, u))
        scanned[row].sort(key = lambda x: x[0])


for row in scanned:
    while True:
        for i, (first_segment, second_segment) in enumerate(pairwise(scanned[row])):
            if first_segment[1] >= second_segment[0] - 1:
                scanned[row][i] = (first_segment[0], max(first_segment[1], second_segment[1]))
                del(scanned[row][i+1])
                break
        else:
            break


part_1 = 0
for line_segment in scanned[UPPER//2]:
    for x in range(line_segment[0], line_segment[1] + 1):
        if (x, UPPER//2) not in beacons:
            part_1 += 1

y_idx = [row for row, segments in scanned.items() if len(segments) > 1][0]
x_idx = scanned[y_idx][0][1]+1

part_2 = x_idx * 4000000 + y_idx

print(f"Part 1: {part_1}")
print(f"Part 2: {part_2}")
