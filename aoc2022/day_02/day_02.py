# Solution of AOC2022 day 1

import tools
from enum import Enum
from dataclasses import dataclass


class Sign(Enum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2


class Answer(Enum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2


class Outcome(Enum):
    LOSE = 0
    DRAW = 1
    WIN = 2


class Round:
    str_to_sign = {
        "A": Sign.ROCK,
        "B": Sign.PAPER,
        "C": Sign.SCISSORS,
    }

    str_to_answer = {
        "X": Answer.ROCK,
        "Y": Answer.PAPER,
        "Z": Answer.SCISSORS,
    }

    str_to_outcome = {
        "X": Outcome.LOSE,
        "Y": Outcome.DRAW,
        "Z": Outcome.WIN,
    }

    outcome_to_points = {
        Outcome.LOSE: 0, 
        Outcome.DRAW: 3, 
        Outcome.WIN: 6, 
    }

    my_answer_to_points = {
        Answer.ROCK: 1,
        Answer.PAPER: 2,
        Answer.SCISSORS: 3,
    }

    result_list = {
        (Sign.ROCK, Answer.ROCK, Outcome.DRAW),
        (Sign.ROCK, Answer.PAPER, Outcome.WIN),
        (Sign.ROCK, Answer.SCISSORS, Outcome.LOSE),
        (Sign.PAPER, Answer.ROCK, Outcome.LOSE),
        (Sign.PAPER, Answer.PAPER, Outcome.DRAW),
        (Sign.PAPER, Answer.SCISSORS, Outcome.WIN),
        (Sign.SCISSORS, Answer.ROCK, Outcome.WIN),
        (Sign.SCISSORS, Answer.PAPER, Outcome.LOSE),
        (Sign.SCISSORS, Answer.SCISSORS, Outcome.DRAW),
    }

    def __init__(self, sign: str, answer: str = "", outcome: str = ""):
        if outcome == "":
            self.__sign = self.str_to_sign[sign]
            self.__answer = self.str_to_answer[answer]
            self.__determine_outcome()
        elif answer == "":
            self.__sign = self.str_to_sign[sign]
            self.__outcome = self.str_to_outcome[outcome]
            self.__determine_answer()

    def compute_points(self) -> int:
        return self.my_answer_to_points[self.__answer] + self.outcome_to_points[self.__outcome]

    def __determine_outcome(self):
        self.__outcome = [x for x in self.result_list if (x[0] == self.__sign and x[1] == self.__answer)][0][2]

    def __determine_answer(self):
        self.__answer = [x for x in self.result_list if (x[0] == self.__sign and x[2] == self.__outcome)][0][1]


    def __repr__(self) -> str:
        ss = f"{str(self.__sign):>16s}"
        ss += f"{str(self.__answer):>16s}"
        ss += f"{str(self.__outcome):>16s}"
        ss += f"{self.__outcome.value:3d}"
        return ss


if __name__ == "__main__":
    data = tools.read_input_file(__file__)
    rounds_data = [entry.split() for entry in data]

    rounds = [Round(sign=entry[0], answer=entry[1]) for entry in rounds_data]
    total_points = sum([r.compute_points() for r in rounds])
    print(total_points)

    rounds = [Round(sign=entry[0], outcome=entry[1]) for entry in rounds_data]
    total_points = sum([r.compute_points() for r in rounds])
    print(total_points)
