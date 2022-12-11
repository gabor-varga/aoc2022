# Solution of AOC2022 day 7

import tools


class Monkey:
    def __init__(self, data):
        self._id = int(data[0].split(" ")[1][:-1])
        self._items = [int(x) for x in data[1].split(": ")[1].split(",")]
        self._op = data[2].split("= ")[1]
        self._divisor = int(data[3].split("divisible by ")[1])
        self._true_target = int(data[4][-1])
        self._false_target = int(data[5][-1])
        self._num_inspect = 0

    def update(self, monkeys):
        for item in self._items:
            item = self._inspect(item)
            target = self._true_target if item % self._divisor == 0 else self._false_target
            monkeys[target].add_item(item)
        self._items = []

    def add_item(self, item):
        self._items.append(item)

    def total_inspections(self):
        return self._num_inspect

    def set_common_divisor(self, common_divisor):
        self._common_divisor = common_divisor

    def divisor(self):
        return self._divisor

    def _inspect(self, old):
        self._num_inspect = self._num_inspect + 1
        tmp = eval(self._op)
        # return tmp // 3
        # mult = tmp // self._divisor
        return tmp % self._common_divisor

    def __repr__(self):
        # ss = ""
        # ss += f"id: {self._id}\n"
        # ss += f"items: {self._items}\n"
        # ss += f"op: {self._op}\n"
        # ss += f"test: {self._divisor}\n"
        # ss += f"true_target: {self._true_target}\n"
        # ss += f"false_target: {self._false_target}\n"
        ss = f"Monkey {self._id}: {self._items}"
        return ss


def multiplyList(myList):
    # Multiply elements one by one
    result = 1
    for x in myList:
        result = result * x
    return result


if __name__ == "__main__":
    data = tools.read_input_file(__file__)
    data = [d.strip() for d in data]

    data_size = 7
    monkey_data = [data[i:i + data_size] for i in range(0, len(data), data_size)]
    # print(monkey_data)

    monkeys = [Monkey(d) for d in monkey_data]
    [print(m) for m in monkeys]
    print()

    common_divisor = multiplyList([m.divisor() for m in monkeys])
    print(common_divisor)

    [m.set_common_divisor(common_divisor) for m in monkeys]

    rounds = 10000
    for i in range(rounds):
        print(i)
        for m in monkeys:
            m.update(monkeys)

        # [print(m) for m in monkeys]
        # print()

    total_inspections = [m.total_inspections() for m in monkeys]
    print(total_inspections)
    out = sorted(total_inspections)
    print(out[-1] * out[-2])
