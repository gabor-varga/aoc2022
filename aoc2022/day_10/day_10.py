# Solution of AOC2022 day 7

import tools
import numpy as np


def update_cycle(cyc: int, reg: int) -> int:
    out = cyc + 1
    # print(out, reg)
    if out in critical_cycles:
        critical_register_values.append(reg)
    
    pos = cyc % 40

    if abs(reg - pos) <= 1:
        print("#", end="")
    else:
        print(".", end="")
    if out % 40 == 0:
        print()
    return out


if __name__ == "__main__":
    data = tools.read_input_file(__file__)

    cycle = 0
    register = 1
    critical_cycles = [20, 60, 100, 140, 180, 220]
    critical_register_values = []

    for line in data:
        # print(line)
        if line == "noop":
            cycle = update_cycle(cycle, register)
        elif "addx" in line:
            val = int(line.split(" ")[1])
            cycle = update_cycle(cycle, register)
            cycle = update_cycle(cycle, register)
            register += val

    # print(critical_cycles)
    # print(critical_register_values)

    # out = sum([c * r for c, r in zip(critical_cycles, critical_register_values)])
    # print(out)
