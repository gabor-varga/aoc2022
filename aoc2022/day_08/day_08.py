# Solution of AOC2022 day 7

import tools
import numpy as np


if __name__ == "__main__":
    data = tools.read_input_file(__file__)

    hex = np.asarray([[int(s) for s in line] for line in data])
    # print(hex)

    rows, cols = np.shape(hex)
    # print(rows, cols)

    # visibility = np.ones(np.shape(hex))
    viewing = np.ones(np.shape(hex))
    # print(visibility)

    for i in range(1, cols - 1):
        for j in range(1, rows - 1):
            # print("hex:", hex[i, j])
            # print("left:", hex[i, :j])
            # print("right:", hex[i, j+1:])
            # print("top:", hex[:i, j])
            # print("bottom:", hex[i+1:, j])

            center = hex[i, j]

            left = hex[i, :j]
            right = hex[i, j+1:]
            top = hex[:i, j]
            bottom = hex[i+1:, j]

            left_max = np.max(left)
            right_max = np.max(right)
            top_max = np.max(top)
            bottom_max = np.max(bottom)

            left_dist = np.argmax(left[::-1] >= center) + 1
            right_dist = np.argmax(right >= center) + 1
            top_dist = np.argmax(top[::-1] >= center) + 1
            bottom_dist = np.argmax(bottom >= center) + 1
            # print(left_dist, right_dist, top_dist, bottom_dist)

            if left_max < center:
                left_dist = len(left)
            if right_max < center:
                right_dist = len(right)
            if top_max < center:
                top_dist = len(top)
            if bottom_max < center:
                bottom_dist = len(bottom)


            # print(left_dist, right_dist, top_dist, bottom_dist)
            viewing[i, j] = left_dist * right_dist * top_dist * bottom_dist

            # left_max = np.max(left)
            # right_max = np.max(right)
            # top_max = np.max(top)
            # bottom_max = np.max(bottom)
            # # print(center, min(left_max, right_max, top_max, bottom_max), left_max, right_max, top_max, bottom_max)
            # if center <= min(left_max, right_max, top_max, bottom_max):
            #     visibility[i, j] = 0
            # # print("visible: ", visibility[i, j])
            # # print()

    # print(visibility)
    # visible_trees = sum(sum(visibility))
    # print(visible_trees)
    
    # print(hex)
    # print(visibility)
    # print(viewing)

    viewing_max = np.max(viewing)
    print(viewing_max)
