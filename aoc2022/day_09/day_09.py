# Solution of AOC2022 day 7

import tools
import numpy as np
import os
import sys
import time


def follow(head, tail):
    delta = head - tail
    if np.max(np.abs(delta)) > 1:
        step = np.clip(delta, -1, 1)
        tail += step


def output(rope):
    m = np.max(np.abs(rope))
    out = ""
    for i in range(-m, m + 1):
        for j in range(-m, m + 1):
            t = [k for k, x in enumerate(rope) if np.all(x == np.asarray([i, j]))]
            if t:
                out += t[0]
            else:
                out += "."
        out += "\n"
    return out


if __name__ == "__main__":
    data = tools.read_input_file(__file__)

    dir_map = {
        "D" : np.asarray((0, -1)),
        "R" : np.asarray((1, 0)),
        "U" : np.asarray((0, 1)),
        "L" : np.asarray((-1, 0)),
    }

    moves = [line.split(" ") for line in data]
    moves = [(dir_map[move[0]], int(move[1])) for move in moves]

    rope_length = 10
    rope = [np.asarray([0, 0]) for i in range(rope_length)]

    tail_trail = [(0, 0)]

    for dir, steps in moves:
        for i in range(steps):
            rope[0] += dir
            for j in range(rope_length - 1):
                follow(rope[j], rope[j + 1])
            # print("head", head)
            # follow(head, tail)
            # print("tail", tail)
            # print()
            end = (rope[-1][0], rope[-1][1])
            tail_trail.append(end)

    print(len(tail_trail))
    tail_trail_unique = list(set(tail_trail))
    print(len(tail_trail_unique))

    # output(rope)

    # os.system(clear_console)

    # # Write the current frame on stdout and sleep
    # sys.stdout.write(output(rope))
    # sys.stdout.flush()
    # time.sleep(0.1)