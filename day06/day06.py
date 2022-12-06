import os

day = os.path.basename(os.getcwd())
stream = open(f"{day}.in").read().strip()

def solve(length):
    for i in range(length, len(stream)):
        if len(set(stream[i-length:i])) == length:
            return i

    
print(f"Part 1: {solve(4)}")
print(f"Part 2: {solve(14)}")
