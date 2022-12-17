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


    def compute_prio(current_valve, target_valve):
        path = g.get_shortest_paths(name_to_id[current_valve.name], to=name_to_id[target_valve.name], output="vpath")
        length = len(path[0]) - 1
        return (26 - length) * target_valve.flow_rate, target_valve.flow_rate, length


    def get_next_prio(current_valve, valves_to_sort):
        valves_prio = [compute_prio(current_valve, v) for v in valves_to_sort]
        out = list(reversed(sorted(zip(valves_prio, valves_to_sort), key=lambda x: x[0][0])))
        # for v in out:
        #     print(v)
        return out[0][1]


    valves_to_open = deepcopy(valves_sorted)
    valves_to_open = list(filter(lambda x: x.flow_rate > 0, valves_to_open))
    print(valves_to_open)

    def advance_time(t, fr, released):
        released += fr
        t += 1
        return t, released

    def compute_total_pressure_released(current_valves, log=False):
        valves = deepcopy(current_valves)
        time = 0
        current = start
        current_flow_rate = 0
        pressure_released = 0

        while (time < 30):
            if valves:
                # next_to_open = get_next_prio(current, valves)
                next_to_open = valves[0]
                # if log:
                #     print(f"Next to open: {next_to_open.name}")

                path = g.get_shortest_paths(name_to_id[current.name], to=name_to_id[next_to_open.name], output="vpath")

                for p in path[0][1:]:
                    time, pressure_released = advance_time(time, current_flow_rate, pressure_released)
                    if log:
                        print(f"Min {time}")
                        print(f"Moving to valve {id_to_name[p]}")
                        print(f"Releasing pressure: {current_flow_rate}")
                        print(f"Total released: {pressure_released}\n")

                time, pressure_released = advance_time(time, current_flow_rate, pressure_released)
                if log:
                    print(f"Min {time}")
                    print(f"Opening valve {next_to_open.name}")
                    print(f"Releasing pressure: {current_flow_rate}")
                    print(f"Total released: {pressure_released}\n")
                current_flow_rate += next_to_open.flow_rate
                valves.remove(next_to_open)
                current = next_to_open
            else:
                time, pressure_released = advance_time(time, current_flow_rate, pressure_released)
                if log:
                    print(f"Min {time}")
                    print(f"Releasing pressure: {current_flow_rate}")
                    print(f"Total released: {pressure_released}\n")

        return pressure_released


    def mutate(valves):
        out = deepcopy(valves)
        l = len(out)
        i1 = random.randint(0, l - 1)
        i2 = random.randint(0, l - 1)
        out[i1], out[i2] = out[i2], out[i1]
        return out


    # print([v.name for v in valves])
    # valves = mutate(valves)
    # print([v.name for v in valves])


    best_valves = deepcopy(valves_to_open)
    # best_valves = [
    #     valves_to_open[2],
    #     valves_to_open[3],
    #     valves_to_open[1],
    #     valves_to_open[0],
    #     valves_to_open[4],
    #     valves_to_open[5],
    # ]
    # print([v.name for v in best_valves])
    best = compute_total_pressure_released(best_valves)
    print(best)

    for i in range(10000):
        valves = mutate(best_valves)
        # print([v.name for v in valves])
        pres = compute_total_pressure_released(valves)
        if pres > best:
            best = pres
            best_valves = deepcopy(valves)
            [print(v) for v in best_valves]
            print(best)

    print(compute_total_pressure_released(best_valves, log=True))