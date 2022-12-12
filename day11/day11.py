import os
import re
from collections import deque
from math import prod

day = os.path.basename(os.getcwd())

def digits(string):
    return [int(x) for x in re.findall(r"\d+", string)]


class Monkey():

    def __init__(self, monkey_input):
        lines = monkey_input.split("\n")

        self.number = digits(lines[0])[0]
        self.items = deque(digits(lines[1]))
        self.operation = lines[2].strip().replace("Operation: new = ", "")
        self.div_by = digits(lines[3])[0]
        self.true_to = digits(lines[4])[0]
        self.false_to = digits(lines[5])[0]
        self.thrown = 0

    def __str__(self) -> str:
        return f"Monkey {self.number}: {', '.join(str(x) for x in self.items)}"
        
    def __repr__(self) -> str:
        return f"Monkey {self.number}"

    def inspect_item(self, item):
        old = item 
        #print(f" Monkey inspects an item with a worry level of {old}.")
        new = eval(self.operation)
        #print(f"  Worry level becomes {new}.")
        new = new % multiplum
        #print(f"  Monkey gets bored with item. Worry level is divided by 3 to {new}.")

        if new % self.div_by == 0:
            #    print(f"  Current worry level is divisible by {self.div_by}.")
            throw_to = self.true_to
        else:
            throw_to = self.false_to
            #print(f"  Current worry level is not divisible by {self.div_by}.")


        #print(f"  Item with worry level {new} is thrown to monkey {throw_to}.")
        return throw_to, new

    def inspect_items(self):
        #print(f"Monkey {self.number}:")
        for i in range(len(self.items)):
            item = self.items.popleft()
            throw_to, worry_level = self.inspect_item(item)
            monkeys[throw_to].items.append(worry_level)
            self.thrown += 1
            


monkeys = [Monkey(m_input) for m_input in open(f"{day}.in").read().split("\n\n")]
multiplum = prod(m.div_by for m in monkeys)
rounds = 10000
for i in range(rounds):
    for m in monkeys:
        m.inspect_items()

    if i == 20:
        print(f"== After round {i} ==")
        for m in monkeys:
            print(f"Monkey {m.number} inspected items {m.thrown} times.")
            print(m)

    if i % 1000 == 0:
        print(f"== After round {i} ==")
        for m in monkeys:
            print(f"Monkey {m.number} inspected items {m.thrown} times.")
            print(m)


print()
for m in monkeys:
    print(m)

m_sort = sorted(monkeys, key = lambda x : x.thrown, reverse=True)

print()
for m in m_sort:
    print(m.thrown)

part_1 = m_sort[0].thrown * m_sort[1].thrown
part_2 = 0


print(f"Part 1: {part_1}")
print(f"Part 2: {part_2}")
