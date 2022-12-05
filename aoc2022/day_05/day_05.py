# Solution of AOC2022 day 1

from typing import List
import tools
import re


class Move:
    def __init__(self, move_info: str):
        m = re.match("move (\\d*) from (\\d*) to (\\d*)", move_info)
        self._amount = int(m.group(1))
        self._source = int(m.group(2)) - 1
        self._destination = int(m.group(3)) - 1

    def amount(self):
        return self._amount

    def source(self):
        return self._source

    def destination(self):
        return self._destination

    def __repr__(self):
        return f"Move {self._amount} From {self._source} To {self._destination}"
    

class Stack:
    def __init__(self, crates: list):
        self._crates = crates
    
    def push(self, crate):
        self._crates.append(crate)
    
    def pop(self):
        if len(self._crates) == 0:
            raise RuntimeError("Stack is empty")
        return self._crates.pop()

    def __repr__(self):
        return f"{' '.join(self._crates)}"


class Ship:
    def __init__(self, stack_data: list):
        self._stacks = [Stack(l) for l in stack_data]
    
    def __getitem__(self, i):
        return self._stacks[i]

    def __repr__(self):
        s = ""
        for i, stack in enumerate(self._stacks):
            s += f"{i + 1} : {stack}\n"
        return s


def apply_move_on_ship_9000(ship: Ship, move: Move):
    for i in range(move.amount()):
        crate = ship[move.source()].pop()
        ship[move.destination()].push(crate)


def apply_move_on_ship_9001(ship: Ship, move: Move):
    crates = [ship[move.source()].pop() for i in range(move.amount())]
    crates.reverse()
    [ship[move.destination()].push(c) for c in crates]


if __name__ == "__main__":
    data = tools.read_input_file(__file__)
    
    idx = [i for i in range(len(data)) if data[i] == ""][0]
    containers = data[:idx-1]

    lists = [list() for i in range(9)]

    for line in containers:
        s = str(line) + " "
        entries = [x for x in zip(*(iter(s),) * 4)]
        for i, e in enumerate(entries):
            crate = str(e[1])
            if crate != " ":
                lists[i].append(crate)

    [l.reverse() for l in lists]
    ship = Ship(lists)

    print(ship)

    moves = [Move(move) for move in data[idx+1:]]

    [apply_move_on_ship_9001(ship, move) for move in moves]

    print(ship)

    print("".join([stack.pop() for stack in ship]))
