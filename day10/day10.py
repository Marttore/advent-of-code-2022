import os

day = os.path.basename(os.getcwd())
lines = [l.split() for l in open(f"{day}.in").read().splitlines()]

cycles = [20, 60, 100, 140, 180, 220]
signal_strength = 0
register = 1
cycle=1
screen = [[" " for _ in range(40)] for _ in range(6)]

def sprite_position(register):
    return (
            register - 1 if register > 0 else None,
            register, 
            register + 1 if register < 39 else None
)

def check(cycle):
    global signal_strength
    if cycle in cycles:
        signal_strength += register * cycle

def increment_cycle(cycle, register):
    row = (cycle-1) // 40
    col = (cycle-1) % 40

    if col in sprite_position(register):
        screen[row][col] = "#"

    return cycle + 1

for l in lines:
    if len(l) == 2:
        cycle = increment_cycle(cycle, register)
        check(cycle)

        cycle = increment_cycle(cycle, register)
        register += int(l[1])
        check(cycle)

    else:
        cycle = increment_cycle(cycle, register)
        check(cycle)

print(f"Part 1: {signal_strength}")
print("Part 2:")
print()
for i in range(6):
    print("".join(screen[i]))
