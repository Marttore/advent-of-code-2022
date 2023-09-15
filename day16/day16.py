import os 
import re
from functools import cache
import time

day = os.path.basename(os.getcwd())

flows = {}
connections = {}
valve_mapping = {}

for i, row in enumerate(open(f"{day}.in")):
    flow = int(re.findall(r"\d+", row)[0])
    valve, *connected = re.findall(r"[A-Z]{2}", row)
    flows[i] = flow
    connections[i] = {c : 1 for c  in connected}
    valve_mapping[valve] = i

for i, c in connections.items():
    connections[i] = {valve_mapping[k]: v for k, v in c.items()}

def contract(curr):
    conn = connections[curr]

    for a in conn:
        for b in conn:
            if a != b:
                if b not in connections[a]:
                    connections[a][b] = connections[curr][b] + connections[curr][a]
        del connections[a][curr]

    del connections[curr]
    del flows[curr]
    curr_map = [k for k,v in valve_mapping.items() if v == curr][0]
    del valve_mapping[curr_map]

zeros = [k for k, v in flows.items() if v == 0 and valve_mapping["AA"] != k]
for z in zeros:
    contract(z)

print(flows)
print(connections)
print(valve_mapping)

def get_bit(value, bit_index):
    return (value >> bit_index) & 1

def set_bit(value, bit_index):
    return value | (1 << bit_index)


@cache
def get_flow(value):
    return sum(flow for k, flow in flows.items() if get_bit(value, k) == 1)


@cache
def iterate(position, open, minute):

    if minute >= 30:
        return 0

    best = 0
    if get_bit(open, position) == 0:
        val = flows[position] * (30 - minute)
        best = iterate(position, set_bit(open, position), minute + 1) + val

    for next_pos, dist in connections[position].items():
        best = max(best, iterate(next_pos, open, minute + dist)) 

    return best

@cache
def iterate2(my_pos, el_pos,my_min, el_min, open):

    if my_min >= 26 and el_min >= 26:
        return 0

    turn  = my_min <= el_min

    best = 0
    if turn:
        if get_bit(open, my_pos) == 0:
            val = flows[my_pos] * (26 - my_min)
            best = iterate2(my_pos, el_pos, my_min + 1, el_min , set_bit(open, my_pos)) + val
    else:
        if get_bit(open, el_pos) == 0:
            val = flows[el_pos] * (26 - el_min)
            best = iterate2(my_pos, el_pos, my_min, el_min + 1 , set_bit(open, my_pos)) + val

    if turn:
        for next_pos, dist in connections[my_pos].items():
            best = max(best, iterate2(next_pos, el_pos, my_min + dist, el_min, open))
    else:
        for next_pos, dist in connections[el_pos].items():
            best = max(best, iterate2(my_pos, next_pos, my_min, el_min + dist, open))

    return best + get_flow(open)

st = time.time()
part_1 = iterate(valve_mapping["AA"], 1, 1)
el_time = time.time() - st
#part_2 = iterate2(valve_mapping["AA"], valve_mapping["AA"],1, 1, 1)
print(part_1)
print(el_time)
#print(part_2)


