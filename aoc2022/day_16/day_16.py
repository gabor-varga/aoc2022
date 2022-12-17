# Solution of AOC2022 day 7

import tools
import re
import igraph as ig
import random
from copy import deepcopy


class Valve:
    def __init__(self, name, flow_rate, tunnels):
        self.name = name
        self.flow_rate = flow_rate
        self.tunnels = tunnels
    
    def __repr__(self):
        return f"{self.name} {self.flow_rate} {self.tunnels}"


if __name__ == "__main__":
    data = tools.read_input_file(__file__)
    
    name_to_id = dict()
    g = ig.Graph()

    valves = list()

    start = None

    iden = 0
    for line in data:
        int_reg = "([-+]?\\d+)"
        m = re.match("Valve (.+) has flow rate=(\\d+); tunnel[s]? lead[s]? to valve[s]? (.+)", line)
        assert(m)
        name = m[1]
        flow_rate = int(m[2])
        tunnels = [x.strip() for x in m[3].split(",")]
        valves.append(Valve(name, flow_rate, tunnels))
        name_to_id[name] = iden
        if name == "AA":
            start = valves[-1]
        iden = iden + 1

    id_to_name = {v: k for k, v in name_to_id.items()}

    valves_sorted = list(reversed(sorted(valves, key = lambda x: x.flow_rate)))
    num_valves = len(valves)

    g.add_vertices(num_valves)
    for v in valves:
        for t in v.tunnels:
            g.add_edge(name_to_id[v.name], name_to_id[t])


    valves_to_open = deepcopy(valves_sorted)
    valves_to_open = list(filter(lambda x: x.flow_rate > 0, valves_to_open))
    
    path_length = dict()
    for i in range(len(valves_to_open)):
        v1 = valves_to_open[i]
        id1 = name_to_id[v1.name]

        for j in range(len(valves_to_open)):
            if i != j:
                v2 = valves_to_open[j]
                id2 = name_to_id[v2.name]
                path = g.get_shortest_paths(id1, id2, output="vpath")
                path_length[v1.name, v2.name] = len(path[0]) - 1
        
        id0 = name_to_id["AA"]
        path = g.get_shortest_paths(id0, id1, output="vpath")
        path_length["AA", v1.name] = len(path[0]) - 1
        

    # for n in path_length:
    #     print(f"{n[0]} to {n[1]} = {path_length[n]}")


    def mutate(valves):
        out = deepcopy(valves)
        l = len(out)
        i1 = random.randint(0, l - 1)
        i2 = random.randint(0, l - 1)
        out[i1], out[i2] = out[i2], out[i1]
        return out

    def compute_cost(first, valves):
        remaining_time = 26
        released = 0
        current = first
        for v in valves:
            time_to_move = path_length[current.name, v.name]
            if remaining_time > time_to_move + 1:
                time_spent = path_length[current.name, v.name] + 1
                remaining_time -= time_spent
                released += remaining_time * v.flow_rate
                current = v
        return released

    def compute_cost2(first, valves1, valves2):
        return compute_cost(first, valves1) + compute_cost(first, valves2)


    def cross_mutate(valves1, valves2):
        out1 = deepcopy(valves1)
        out2 = deepcopy(valves2)
        l1 = len(out1)
        l2 = len(out2)
        i1 = random.randint(0, l1 - 1)
        i2 = random.randint(0, l2 - 1)
        out1[i1], out2[i2] = out2[i2], out1[i1]
        return out1, out2


    def mutate2(valves1, valves2):
        valves1 = mutate(valves1)
        valves2 = mutate(valves2)
        valves1, valves2 = cross_mutate(valves1, valves2)
        return valves1, valves2


    best_best = 0
    for k in range(100):
        best_valves = deepcopy(valves_to_open)
        random.shuffle(best_valves)
        best = compute_cost(start, best_valves)
        best_valves_1 = []
        best_valves_2 = []
        for v in best_valves:
            best_valves_1.append(v) if bool(random.getrandbits(1)) else best_valves_2.append(v)


        for i in range(10000):
            valves_1, valves_2 = mutate2(best_valves_1, best_valves_2)
            # print([v.name for v in valves])
            pres = compute_cost2(start, valves_1, valves_2)
            if pres > best:
                best = pres
                best_valves_1 = deepcopy(valves_1)
                best_valves_2 = deepcopy(valves_2)
                # [print(v) for v in best_valves]

        b = compute_cost2(start, best_valves_1, best_valves_2)
        if b > best_best:
            best_best = b
            print(b)
    
    print(best_best)
