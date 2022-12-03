# Solution of AOC2022 day 1

import tools
from more_itertools import split_at
import operator


if __name__ == "__main__":
    data = tools.read_input_file(__file__)

    numbers = [int(d) if d else None for d in data]
    elves = [x for x in split_at(numbers, operator.not_)]

    elves_total = [sum(elf) for elf in elves]
    elves_total_sorted = sorted(elves_total)

    print(elves_total_sorted[-1])
    print(sum(elves_total_sorted[-3:]))
