# Solution of AOC2022 day 1

import tools


if __name__ == "__main__":
    data = tools.read_input_file(__file__)
    comms = data[0]
    
    num = 14
    for i in range(num, len(comms)):
        if sorted(list(set(comms[i-num:i]))) == sorted(list(comms[i-num:i])):
            print(i)
            break
