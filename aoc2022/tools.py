# Tools for AOC2022

import os


def read_input_file(file_path):
    path = file_path.split("/")
    problem = path[-2]
    directory = "/".join(path[:-1])
    problem_input = f"{directory}/{problem}.txt"

    with open(problem_input) as file:
        data = [line.rstrip() for line in file]
    
    return data
