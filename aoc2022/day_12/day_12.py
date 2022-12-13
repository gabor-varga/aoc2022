# Solution of AOC2022 day 7

import tools
import numpy as np


if __name__ == "__main__":
    data = tools.read_input_file(__file__)
    
    start_pos = [-1, -1]
    goal_pos = [-1, -1]

    def get_height(x, i, j):
        if x == "S":
            start_pos[0] = j
            start_pos[1] = i
            return 0
        if x == "E":
            goal_pos[0] = j
            goal_pos[1] = i
            return 25
        return ord(x) - ord("a")

    height = np.asarray([[get_height(x, i, j) for i, x in enumerate(line)] for j, line in enumerate(data)])
    shape = np.shape(height)

    advance = list()
    advance.append(list())
    advance[-1].append(goal_pos)
    visited = list()
    visited.append(goal_pos)

    def explore(pos):
        i = pos[0]
        j = pos[1]
        current_height = height[i, j]

        to_explore = list()
        if i > 0:
            to_explore.append([i - 1, j])
        if j > 0:
            to_explore.append([i, j - 1])
        if i < shape[0] - 1:
            to_explore.append([i + 1, j])
        if j < shape[1] - 1:
            to_explore.append([i, j + 1])

        for target in to_explore:
            if target not in visited:
                if height[target[0], target[1]] >= current_height - 1:
                    advance[-1].append([target[0], target[1]])
                    visited.append([target[0], target[1]])

    ctr = 0

    def reached_lowest(phase):
        for pos in phase:
            if height[pos[0], pos[1]] == 0:
                return True
        return False

    while not reached_lowest(advance[-1]):
    # while start_pos not in advance[-1]:
        advance.append(list())
        for pos in advance[-2]:
            explore(pos)
        # for i, phase in enumerate(advance):
        #     print(i, phase)
        # print(len(advance[-1]))
        ctr = ctr + 1
        # print(ctr)

        # for i in range(shape[0]):
        #     for j in range(shape[1]):
        #         if [i, j] in advance[-1]:
        #             print("#", end="")
        #         else:
        #             # print(data[i][j], end="")
        #             print(".", end="")
        #     print()
        # input()
    
    print(len(advance) - 1)
