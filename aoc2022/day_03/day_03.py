# Solution of AOC2022 day 1

import tools


def compute_priority(item: str):
    val_a = ord("a")
    val_A = ord("A")
    num_chars = 26

    code = ord(item)
    value = code - val_a if code >= val_a else code - val_A + num_chars
    value = value + 1
    return value


class Compartment:
    def __init__(self, contents: str):
        self.__contents = sorted(contents)

    def contents(self):
        return self.__contents

    def __repr__(self):
        return "".join(self.__contents)


class Rucksack:
    def __init__(self, contents: str):
        half_size = int(len(contents)/2)
        self._c1 = Compartment(contents[:half_size])
        self._c2 = Compartment(contents[half_size:])
        self.__contents = sorted(contents)

    def contents(self):
        return self.__contents

    def find_common_item(self):
        for i1 in self._c1.contents():
            for i2 in self._c2.contents():
                if i1 == i2:
                    return i1

    def compute_value(self):
        c = self.find_common_item()
        return compute_priority(c)

    def __repr__(self):
        return f"{self._c1} | {self._c2}"


class Group:
    def __init__(self, r1: Rucksack, r2: Rucksack, r3: Rucksack):
        self._r1 = r1
        self._r2 = r2
        self._r3 = r3
    
    def find_common_item(self):
        for i1 in self._r1.contents():
            for i2 in self._r2.contents():
                if i1 == i2:
                    for i3 in self._r3.contents():
                        if i1 == i3:
                            return i1

    def compute_value(self):
        c = self.find_common_item()
        return compute_priority(c)


if __name__ == "__main__":
    data = tools.read_input_file(__file__)
    rucksacks = [Rucksack(entry) for entry in data]
    
    output = sum(r.compute_value() for r in rucksacks)
    print(output)

    groups = [Group(rucksacks[n], rucksacks[n+1], rucksacks[n+2]) for n in range(0, len(rucksacks), 3)]
    output = sum(g.compute_value() for g in groups)
    print(output)
