import os
from copy import deepcopy 

day = os.path.basename(os.getcwd())

KEY = 811589153

numbers = list(map(int, open(f"{day}.in").read().splitlines()))
N = len(numbers)

def mix(numbers, times):
    place = [n for n in range(N)]
    for _ in range(times):
        for i, number in enumerate(numbers):
            if number==0:
                continue

            idx = place.index(i)
            place.pop(idx)
            new_idx =  (idx + number) % (N - 1)
            place.insert(new_idx, i)

    return [numbers[i] for i in place]

output = mix(numbers, 1)
part_1 =  sum(output[i] for i in ((output.index(0)+m) % N for m in [1000, 2000, 3000]))
numbers = [n*KEY for n in numbers]
output = mix(numbers, 10)
part_2 = sum(output[i] for i in ((output.index(0)+m) % N for m in [1000, 2000, 3000]))

print(f"Part 1: {part_1}")
print(f"Part 2: {part_2}")
