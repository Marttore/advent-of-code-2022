import os
import operator

day = os.path.basename(os.getcwd())
monkeys_raw = [m.replace(":", "").split() for m in open(f"{day}.in").read().splitlines()]

opp_op = {
    operator.add : operator.sub,
    operator.sub : operator.add,
    operator.mul : operator.truediv,
    operator.truediv : operator.mul,
}

class Monkey():

    def __init__(self, name, rest):
        self.name = name
        if len(rest) == 1:
            self.value = int(rest[0])
        else:
            self.dependents = (rest[0], rest[2])
            self.value = None
            match rest[1]:
                case "+":
                    self.op = operator.add
                case "-":
                    self.op = operator.sub
                case "*":
                    self.op = operator.mul
                case "/":
                    self.op = operator.truediv
                case _:
                    raise ValueError
            self.org_op = rest[1]

    def update_value(self):
        if self.value is not None:
            return

        try:
            monkeys[self.dependents[0]].update_value()
        except AttributeError:
            pass

        try: 
            monkeys[self.dependents[1]].update_value()
        except AttributeError:
            pass


        if monkeys[self.dependents[0]].value is not None and monkeys[self.dependents[1]].value is not None:
            self.value = int(self.op(monkeys[self.dependents[0]].value, monkeys[self.dependents[1]].value))
 



monkeys = {mname: Monkey(mname, rest) for mname, *rest in monkeys_raw}
monkeys["root"].update_value()
part_1 =  monkeys["root"].value

monkeys = {mname: Monkey(mname, rest) for mname, *rest in monkeys_raw}
monkeys["humn"].value = None
monkeys["root"].update_value()

m1 = monkeys[monkeys["root"].dependents[0]]
m2 = monkeys[monkeys["root"].dependents[1]]

current_val =  m2.value if m1.value is None else m1.value
current = m1 if m1.value is None else m2

while True:

    if not hasattr(current, "dependents"):
        break

    m1 = monkeys[current.dependents[0]]
    m2 = monkeys[current.dependents[1]]
    op = current.op 

    if m1.value is None:
        current_val = opp_op[op](current_val, m2.value)
        current = m1
    else:
        if op == operator.add or op == operator.mul:
            current_val = opp_op[op](current_val, m1.value)
        else:
            current_val = op(m1.value, current_val)
        current = m2
    
    
part_2 = int(current_val)

print(f"Part 1: {part_1}")
print(f"Part 2: {part_2}")
