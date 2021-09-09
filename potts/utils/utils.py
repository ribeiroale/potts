# =========================================================================== #
#                                  utils.py                                   #
# =========================================================================== #

"""Collection of small Python functions and classes which make common patterns 
in the 'potts' package shorter and easier"""

# =========================================================================== #
#                                   Imports                                   #
# =========================================================================== #


# =========================================================================== #
#                                   Classes                                   #
# =========================================================================== #


class SingTrm:
    """Class used to represent singularity functions.

    From <https://en.wikipedia.org/wiki/Singularity_function>:
        Singularity functions are a class of discontinuous functions that
        contain singularities, i.e. they are discontinuous at their singular
        points.

    Attributes
    ----------
    coef : float
           constant multiplying the singularity function
    a    : float
           denotes where in the singularity function either acts or begins to act
    expo : int
           defines the desired discontinuous function
    """

    def __init__(self, coef: float, a: float, expo: float) -> None:
        """
        Attributes
        ----------
        coef : float
               constant multiplying the singularity function
        a    : float
               denotes where in the singularity function either acts or begins to act
        expo : int
               defines the desired discontinuous function
        """
        if expo < -2:
            raise ValueError("Unsupported value for 'expo' < -2")
        else:
            self.expo = expo
        self.a = a
        self.coef = coef

    def __call__(self, x: float) -> float:
        """Evaluate the singularity function at point 'x'.

        Parameters
        ----------
        x : float
            variable of interest
        """
        if self.expo < 0:
            return self.coef if x == self.a else 0
        elif self.expo == 0:
            return 0 if x < self.a else self.coef * 1
        else:
            return 0 if x < self.a else self.coef * (x - self.a) ** self.expo

    def __repr__(self) -> str:
        return f"SingTrm({self.coef}, {self.a}, {self.expo})"

    def __str__(self) -> str:
        return f"{self.coef} * <x - {self.a}> ^ {self.expo}"


# =========================================================================== #
#                                  Functions                                  #
# =========================================================================== #


def integrate(x: SingTrm) -> SingTrm:
    if x.expo < 0:
        return SingTrm(x.coef, x.a, x.expo + 1)
    else:
        return SingTrm(x.coef / (x.expo + 1), x.a, x.expo + 1)


def linear_spacing(start: float, end: float, num_points: int = 100,
                   end_point: bool = True, ret_step: bool = False):
    """Return evenly spaced numbers of a given interval.

    Returns a list containing 'num_points' evenly spaced numbers over the
    specified ['start', 'end'] interval.

    The 'end_point' of the interval can optionally be excluded.
    """

    end = float(end)
    start = float(start)
    spaces = (num_points - 1) if end_point else num_points

    step = (end - start) / spaces
    rv = [start]

    while len(rv) < num_points:
        rv.append(rv[-1] + step)

    if end_point:
        rv[-1] = end

    if ret_step:
        return rv, step
    else:
        return rv
