# =========================================================================== #
#                                   load.py                                   #
# =========================================================================== #

"""Basic Load Analysis Module"""

# =========================================================================== #
#                                   Imports                                   #
# =========================================================================== #

from potts.utils.utils import linear_spacing, SingTrm
from typing import List

# =========================================================================== #
#                                   Classes                                   #
# =========================================================================== #


class Load:
    def __init__(self, loads: List[SingTrm]) -> None:
        self.loads = loads

    def __call__(self, x: float):
        return sum([i(x) for i in self.loads])


class LoadingCase:
    def __init__(self) -> None:
        self.loads = list()
        self.supports = list()

    def set_length(self, length: float) -> None:
        self.length = length

    def add_supports(self, supports) -> None:
        for support in supports:
            self.supports.append(support)
        self.supports.sort()

    def add_loads(self, loads, category: str) -> None:
        for load in loads:
            self.loads.append(load)
        self.loads.sort(key=lambda load: load[1])

    def solve(self, num_points=100) -> None:
        x = linear_spacing(0, self.length, num_points)
        self.reactions = self.reaction()
        self.shear_diagram = [self.shear(_) for _ in x]
        self.bend_diagram = [self.bending(_) for _ in x]

    def reaction(self) -> list:
        # Improve this looping
        # loads[i][0] -> magn, loads[i][1] -> x_pos
        R1 = sum(
            [
                self.loads[i][0] * (1 - self.loads[i][1] / self.length)
                for i in range(len(self.loads))
            ]
        )
        R2 = sum(
            [
                self.loads[i][0] * (self.loads[i][1] / self.length)
                for i in range(len(self.loads))
            ]
        )

        return [R1, R2]

    def shear(self, x):
        rv = 0
        for load in self.loads:
            magn = load[0]
            x_pos = load[1]
            if 0 <= x <= x_pos:
                ret = magn * (1 - x_pos / self.length)
            elif x_pos < x <= self.length:
                ret = -magn * x_pos / self.length
            rv += ret
        return rv

    def bending(self, x):
        # magn, x_pos, length
        # const = self.reactions[0] * x
        rv = 0
        for load in self.loads:
            # load[0] -> magn
            # load[1] -> x_pos
            magn = load[0]
            x_pos = load[1]
            if 0 <= x <= x_pos:
                ret = magn * (self.length - x_pos) * x / self.length
            elif x_pos < x <= self.length:
                ret = magn * x_pos * (1 - x / self.length)
            rv += ret
        return rv

    def __repr__(self) -> str:
        return "LoadingCase()"
