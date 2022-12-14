# Solution of AOC2022 day 7

import tools
import numpy as np


if __name__ == "__main__":
    data = tools.read_input_file(__file__)
    

    x = np.zeros((1000, 200), dtype=int)
    sand_start = np.asarray([500, 0])
    x[sand_start[0], sand_start[1]] = 10

    def get_block(d):
        l = d.split(",")
        return np.asarray([int(l[0]), int(l[1])])

    max_y = 0
    for line in data:
        blocks = line.split(" -> ")
        for b1, b2 in zip(blocks[:-1], blocks[1:]):
            b1_c = get_block(b1)
            b2_c = get_block(b2)
            delta = b2_c - b1_c
            direction = np.sign(delta)
            for i in range(np.max(np.abs(delta)) + 1):
                c = b1_c + i * direction
                x[c[0], c[1]] = 1
                if c[1] > max_y:
                    max_y = c[1]

    for i in range(0, 1000):
        x[i, max_y + 2] = 1

    output_decode = {
        0: ".",
        1: "#",
        2: "o",
        3: "~",
        10: "+",
    }

    def output(left, right, bottom):
        for j in range(0, bottom + 1):
            for i in range(left, right + 1):
                print(output_decode[x[i, j]], end="")
            print()
    
    # output(480, 580, 200)
    output(490, 505, 12)

    max_depth = 199

    def is_below_rock_or_sand(coord, offset):
        return 1 <= x[coord[0] + offset, coord[1] + 1] <= 2

    def is_sand_stopped_by_rock_or_sand(coord):
        return is_below_rock_or_sand(coord, -1) and is_below_rock_or_sand(coord, 0) and is_below_rock_or_sand(coord, 1)

    def add_sand():
        s = np.copy(sand_start)
        # print(s)
        ctr = 0
        while s[1] != max_depth and not is_sand_stopped_by_rock_or_sand(s):
            if not is_below_rock_or_sand(s, 0):
                s += [0, 1]
            elif not is_below_rock_or_sand(s, -1):
                s += [-1, 1]
            elif not is_below_rock_or_sand(s, 1):
                s += [1, 1]
            ctr = ctr + 1
            # print(ctr)
            # print(s)
            # input()

        if s[1] != max_depth:
            x[s[0], s[1]] = 2
            if np.all(s == sand_start):
                return True
        else:
            return True
    
    ctr = 0
    while not add_sand():
        # output(480, 580, max_y + 2)
        ctr = ctr + 1
        print(ctr)
