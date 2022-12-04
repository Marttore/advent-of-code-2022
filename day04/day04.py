class SectionRange():
    def __init__(self, section_range):
        self.start, self.stop = section_range.split("-")
        self.start = int(self.start)
        self.stop = int(self.stop)

    def fully_contained_by(self, other):
        return self.start >= other.start and self.stop <= other.stop

    def overlaps(self, other):
        return not (self.stop < other.start or self.start > other.stop)

    @classmethod 
    def mutually_contains(cls, first, second):
        return first.fully_contained_by(second) or second.fully_contained_by(first)


lines = [x.split(",") for x in open("day04.in").read().splitlines()]
sections = [(SectionRange(x), SectionRange(y)) for x, y in lines]

part_1 = sum(SectionRange.mutually_contains(x, y) for x,y in sections)
part_2 = sum(x.overlaps(y) for x,y in sections)

print(f"Part 1: {part_1}")
print(f"Part 2: {part_2}")

