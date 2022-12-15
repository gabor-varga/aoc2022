# Solution of AOC2022 day 7

import tools
from typing import Tuple, List
import re


class Band:
    def __init__(self, start, end):
        if end < start:
            raise RuntimeError("Negative bound")
        self._start = start
        self._end = end

    def start(self):
        return self._start

    def end(self):
        return self._end

    def width(self):
        return self._end - self._start + 1

    def contains(self, x: int):
        return x >= self._start and x <= self._end
    
    def __repr__(self):
        return f"{self._start} - {self._end}"


def is_overlapping(b1: Band, b2: Band):
    return not (b1.end() < b2.start() or b2.end() < b1.start())


def merge(b1: Band, b2: Band):
    b = Band(min(b1.start(), b2.start()), max(b1.end(), b2.end()))
    # print(f"Merging {b1} and {b2} to get {b}")
    return b


class MultiBand:
    def __init__(self, bands: List[Band]):
        self._bands = self._simplify(bands)

    def width(self):
        return sum((b.width() for b in self._bands))

    def contains(self, x: int):
        return any([b.contains(x) for b in self._bands])
    
    def num_band(self):
        return len(self._bands)

    def bands(self):
        return self._bands

    def _simplify(self, bands: List[Band]):
        out = []

        def is_any_overlap(current_bands):
            for i, b1 in enumerate(current_bands):
                for j, b2 in enumerate(current_bands[i + 1:]):
                    if is_overlapping(b1, b2):
                        return True
            return False
        
        out = bands
        while (is_any_overlap(out)):
            for i, b1 in enumerate(out):
                for j, b2 in enumerate(out[i + 1:]):
                    if is_overlapping(b1, b2):
                        # print(len(out))
                        out[i] = merge(b1, b2)
                        # print(f"Deleting {out[i + j + 1]}")
                        del out[i + j + 1]
                        break
                else:
                    continue
                break
        
        return out


    def __repr__(self):
        return ", ".join([b.__repr__() for b in self._bands])


class Sensor:
    def __init__(self, loc: Tuple[int, int], radius: int):
        self._loc = loc
        self._radius = radius
    
    def x(self):
        return self._loc[0]

    def y(self):
        return self._loc[1]

    def get_band(self, y: int):
        dist = abs(y - self._loc[1])
        remain = self._radius - dist
        if remain >= 0:
            return Band(self._loc[0] - remain, self._loc[0] + remain)
        else:
            return None


if __name__ == "__main__":
    data = tools.read_input_file(__file__)
    
    sensors = list()
    beacons = list()
    for line in data:
        int_reg = "([-+]?\\d+)"
        m = re.match(f"Sensor at x={int_reg}, y={int_reg}: closest beacon is at x={int_reg}, y={int_reg}", line)
        sensor = (int(m[1]), int(m[2]))
        beacon = (int(m[3]), int(m[4]))
        radius = abs(beacon[0] - sensor[0]) + abs(beacon[1] - sensor[1])
        sensors.append(Sensor(sensor, radius))
        beacons.append(beacon)

    beacons = list(set(beacons))


    def get_multiband_at(y: int):
        bands = list(filter(lambda x: x, [s.get_band(y) for s in sensors]))
        return MultiBand(bands)

    y0 = 2000000
    mb = get_multiband_at(y0)
    print(mb)
    w = mb.width()

    for s in sensors:
        if s.y() == y0:
            if mb.contains(s.x()):
                w = w - 1
    for b in beacons:
        if b[1] == y0:
            if mb.contains(b[0]):
                w = w - 1
    
    print(w)

    max_coord = 4000000
    for y in range(max_coord):
        mb = get_multiband_at(y)
        num_band = mb.num_band()
        if num_band > 1:
            x = mb.bands()[0].end() + 1
            f = 4000000 * x + y
            print(f)
        
