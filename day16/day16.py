import os
import re
from copy import deepcopy
from collections import deque
from typing import Dict

day = os.path.basename(os.getcwd())

class Node():
    
    def __init__(self, row):
        flow = int(re.findall(r"\d+", row)[0])
        valve, *connected = re.findall(r"[A-Z]{2}", row)
        connected  = {c : 1 for c in connected}
        self.flow = flow
        self.connected = connected
        self.name = valve
        self.open = False
        self.times_visited = 0
        self.value = 0

    def __hash__(self) -> int:
        return hash(self.name)
    
    def __str__(self) -> str:
        return f"{self.name} : {self.flow}, {self.connected}"
    
    def __repr__(self) -> str:
        return f"{self.name} {self.open}"

    def update_value(self, minute):
        self.value = (30 - minute) * self.flow




valves : Dict[str, Node] = {}
for row in open(f"{day}.test"):
    new_valve = Node(row)
    valves[new_valve.name] = new_valve

def contract(valves, valve):
    connections = valve.connected

    for a in connections:
        for b in connections:
            if a != b:
                valves[a].connected[b] = valve.connected[b] + valve.connected[a]
        del valves[a].connected[valve.name]

    del valves[valve.name]
    return valves

zero_valves = {k: v for k, v in valves.items() if v.flow == 0 and v.name!="AA"} 

for zv in zero_valves.values():
    valves = contract(valves, zv)

for k, valve in valves.items():
    print(valve)

def total_flow(valves):
    return sum(valve.value for valve in valves.values())

BEST = 0
def iterate(valves: Dict[str, Node], minute, position, total):
    valves[position].times_visited += 1
    global BEST

    if minute >= 30:
        if total > BEST:
            BEST = total
        return

    #if total + (30-minute) * 150 < BEST:
    #    return

    if not valves[position].open and valves[position].flow > 0:
        valves_copy = deepcopy(valves)
        valves_copy[position].open = True
        valves_copy[position].update_value(minute)
        new_total = valves_copy[position].value + total
        valves_copy[position].flow=0



        if all(valve.open for valve in valves_copy.values() if valve.flow > 0) :
            if new_total > BEST:
                BEST = total
                return 
        valves_copy[position].times_visited -= 1
        iterate(valves_copy, minute + 1, position, new_total)

    candidates = [(possible_move, dist, valves[possible_move].flow) for possible_move, dist in valves[position].connected.items()]
    candidates.sort(key=lambda x: x[2], reverse=True)
    for possible_move, dist, flow in candidates:
        if valves[possible_move].times_visited >= len(valves[possible_move].connected):
            continue

        valves_copy = deepcopy(valves)

        if valves_copy[position].flow == 0:
            valves_copy = contract(valves_copy, valves[position])

        if minute + dist > 30:
            if  total > BEST:
                BEST = total
            return 
        iterate(valves_copy, minute+dist,  possible_move, total)




def iterate_BFS(org_valves: Dict[str, Node]):
    global BEST
    Q = deque()
    Q.append((org_valves, "AA", 1, 0, None))

    max_flow = max(v.flow for v in org_valves.values())
    while Q:
        valves, position, minute, total, prev = Q.popleft()
        valves[position].times_visited += 1

        if total + (30-minute) * 120 < 1750:
            continue

        if minute >= 30:
            total = total_flow(valves)
            if total > BEST:
                BEST = total
            continue
            
        if not valves[position].open and valves[position].flow > 0:
            valves_copy = deepcopy(valves)
            valves_copy[position].open = True
            valves_copy[position].update_value(minute)
            new_total = valves_copy[position].value


            if all(valve.open for valve in valves_copy.values() if valve.flow > 0) :
                total = total_flow(valves_copy)
                if total > BEST:
                    BEST = total
                continue
            

            if new_total > BEST:
                BEST=new_total

            valves_copy[position].times_visited -= 1
            Q.append((valves_copy, position, minute + 1, new_total, prev))

        candidates = [(possible_move, dist, valves[possible_move].flow) for possible_move, dist in valves[position].connected.items()]
        candidates.sort(key=lambda x: x[2], reverse=True)
        for possible_move, dist, flow in candidates:
            if valves[possible_move].times_visited >= len(valves[possible_move].connected):
                continue

            if possible_move == prev:
                continue

            valves_copy = deepcopy(valves)

            Q.append((valves_copy, possible_move,  minute+dist, total, position))

        #if len(valves[possible_move].connected) == 1:
        if prev:
            if valves[prev].times_visited < len(valves[prev].connected):

                valves_copy = deepcopy(valves)
                Q.append((valves_copy, prev, minute+valves[position].connected[prev], total, position ))



iterate(valves, 1, "AA", 0)
#iterate_BFS(valves)
print(f"Part 1: {BEST}")