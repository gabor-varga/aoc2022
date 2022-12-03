# Get input data for day N

import argparse
import os
from aocd.models import Puzzle


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="get_input_data", description="AOC 2022 input fetcher"
    )

    parser.add_argument("day", type=int)  # positional argument
    args = parser.parse_args()
    
    puzzle = Puzzle(year=2022, day=args.day)
    token = f"day_{args.day:02d}"
    filepath = f"{token}/{token}.txt"
    os.makedirs(token)
    with open(filepath, "w") as file:
        file.write(puzzle.input_data)
