rounds = [x.split() for x in open("day2.in")]

theirs = ["A", "B", "C"]
ours = ["X", "Y", "Z"]

def calculate_score_part1(their, our):
    score = 0 

    their_index = theirs.index(their)
    our_index  = ours.index(our)

    if their_index == our_index:
        score += 3
    elif (their_index + 1) % 3 == our_index:
        score += 6

    return score + our_index + 1

def calculate_score_part2(their, outcome):
    score = 0 

    their_index = theirs.index(their)

    if outcome=="Y":
        score += 3
        our_index = their_index
    elif outcome=="Z":
        score += 6
        our_index = (their_index + 1) % 3
    else:
        score += 0
        our_index = (their_index - 1) % 3

    return score + our_index + 1


part1 = sum([calculate_score_part1(x, y) for x, y in rounds])
part2 = sum([calculate_score_part2(x, y) for x, y in rounds])

print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
