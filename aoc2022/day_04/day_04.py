# Solution of AOC2022 day 1

import tools


class Assignment:
    def __init__(self, sector_info: str):
        tmp = sector_info.split("-")
        self._sector_start = int(tmp[0])
        self._sector_end = int(tmp[1])
    
    def start(self) -> int:
        return self._sector_start

    def end(self) -> int:
        return self._sector_end


def is_assignment_contained_in(left: Assignment, right: Assignment) -> bool:
    return left.start() >= right.start() and left.end() <= right.end()


def are_assignments_inclusive(left: Assignment, right: Assignment) -> bool:
    return is_assignment_contained_in(left, right) or is_assignment_contained_in(right, left)


def are_assignments_overlapping(left: Assignment, right: Assignment) -> bool:
    return not(left.end() < right.start() or right.end() < left.start())


if __name__ == "__main__":
    data = tools.read_input_file(__file__)
    
    elf_pairs = (entry.split(",") for entry in data)
    assignments = [(Assignment(entry[0]), Assignment(entry[1])) for entry in elf_pairs]
    total_inclusive = sum((are_assignments_inclusive(ass1, ass2) for ass1, ass2 in assignments))
    print(total_inclusive)

    total_overlapping = sum((are_assignments_overlapping(ass1, ass2) for ass1, ass2 in assignments))
    print(total_overlapping)
