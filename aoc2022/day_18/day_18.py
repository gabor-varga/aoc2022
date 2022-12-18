# Solution of AOC2022 day 7

import tools
import numpy as np
from copy import deepcopy
import sys


if __name__ == "__main__":
    sys.setrecursionlimit(10000)

    data = tools.read_input_file(__file__)

    coords = np.asarray([np.asarray([int(x) for x in line.split(",")]) for line in data])

    max_size = [(np.min(coords[:, i]), np.max(coords[:, i])) for i in range(3)]
    # print(max_size)
    width = [max_size[i][1] - max_size[i][0] + 1 for i in range(3)]
    # print(width)
    volume = width[0] * width[1] * width[2]
    # print(volume)


    block = np.zeros((max_size[0][1] + 2, max_size[1][1] + 2, max_size[2][1] + 2))

    for c in coords:
        block[c[0], c[1], c[2]] = 1

    all_dirs = [
        np.asarray([-1,  0,  0]),
        np.asarray([ 1,  0,  0]),
        np.asarray([ 0, -1,  0]),
        np.asarray([ 0,  1,  0]),
        np.asarray([ 0,  0, -1]),
        np.asarray([ 0,  0,  1]),
    ]


    water = list()

    sh = np.shape(block)

    def check_water(current):
        for dir in all_dirs:
            c = list(np.asarray(current) + dir)
            # print(f"Checking: {c}")
            # print([max_size[i][0] for i in range(3)])
            # print([max_size[i][1] for i in range(3)])
            # print([c[i] >= max_size[i][0] and c[i] <= max_size[i][1] for i in range(3)])
            if all([c[i] >= 0 and c[i] < sh[i] for i in range(3)]):
                # print(f"Inside: {c}")
                if not block[c[0], c[1], c[2]] and c not in water:
                    water.append(c)
                    check_water(c)
    
    start = [max_size[i][0] for i in range(3)]
    water.append(start)
    check_water(start)

    for w in water:
        if block[w[0], w[1], w[2]] == 1:
            raise RuntimeError("Error")
        block[w[0], w[1], w[2]] = 2


    # for i in range(sh[0]):
    #     for j in range(sh[1]):
    #         for k in range(sh[2]):
    #             c = "."
    #             if block[i, j, k] == 1:
    #                 c = "#"
    #             if block[i, j, k] == 2:
    #                 c = "O"
    #             print(c, end="")
    #             # print(i, j, k)
    #             # ctr += 1
    #             # print(ctr)
    #         print()
    #     print()
    #     input()


    sides = np.zeros(len(coords))

    for i, c in enumerate(coords):
        for dir in all_dirs:
            d = list(c + dir)
            # if block[d[0], d[1], d[2]] != 1:
            if block[d[0], d[1], d[2]] == 2:
                sides[i] += 1
    
    exposed = sum(sides)
    print(exposed)
