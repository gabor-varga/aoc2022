# Solution of AOC2022 day 7

import tools


if __name__ == "__main__":
    data = tools.read_input_file(__file__)
    
    entries = [data[i:i+3] for i in range(0, len(data), 3)]

    def compare(x1, x2):
        # print(f"x1 = {x1}")
        # print(f"x2 = {x2}")
        if type(x1) == int and type(x2) == int:
            return x1 - x2

        elif type(x1) == list and type(x2) == list:
            for y1, y2 in zip(x1, x2):
                cmp = compare(y1, y2)
                if cmp != 0:
                    return cmp
            return len(x1) - len(x2)

        elif type(x1) != type(x2):
            if type(x1) == int:
                x1 = [x1]
            elif type(x2) == int:
                x2 = [x2]

        cmp = compare(x1, x2)
        return cmp


    out = list()
    for i, entry in enumerate(entries):
        p1 = eval(entry[0])
        p2 = eval(entry[1])
        # print(p1)
        # print(p2)

        cmp = compare(p1, p2)
        # print(cmp)
        # print()

        if cmp < 0:
            out.append(i + 1)
        
    # print(out)
    print(sum(out))


    all_packets = list(filter(lambda x: x is not None, [eval(entry) if len(entry) else None for entry in data]))
    all_packets.append([[2]])
    all_packets.append([[6]])

    from functools import cmp_to_key
    all_packets_sorted = list(sorted(all_packets, key=cmp_to_key(compare)))
    
    id1 = -1
    id2 = -1
    for i, p in enumerate(all_packets_sorted):
        if p == [[2]]:
            id1 = i + 1
        if p == [[6]]:
            id2 = i + 1
    
    print(id1 * id2)
