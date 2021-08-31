# =========================================================================== #
#                                  utils.py                                   #
# =========================================================================== #

"""Collection of small Python functions and classes which make common patterns 
in the 'potts' package shorter and easier"""

# =========================================================================== #
#                                   Imports                                   #
# =========================================================================== #

from numbers import Real

# =========================================================================== #
#                                   Classes                                   #
# =========================================================================== #


class Singularity:
    """Class used to represent singularity functions.

    From <https://en.wikipedia.org/wiki/Singularity_function> :
        Singularity functions are a class of discontinuous functions that
        contain singularities, i.e. they are discontinuous at their singular
        points.

    Attributes
    ----------
    a : float
        denotes where in the singularity function either acts or begins to act
    n : int
        defines the desired discontinuous function
    """

    def __init__(self, a: float, n: int) -> None:
        """
        Parameters
        ----------
        a : float
            denotes where in the singularity function either acts or begins to act
        n : int
            defines the desired discontinuous function
        """
        self.a = a
        self.n = n
        self._const = 1.0

    def __call__(self, x) -> Real:
        """Evaluate the singularity function at point 'x'.

        Parameters
        ----------
        x : float
            variable of interest
        """
        return 0 if x <= self.a else self._const * (x - self.a) ** self.n

    def integrate(self) -> None:
        """Integrate the singularity function in-place."""
        if self.n < 0:
            self.n = self.n + 1
        else:
            self.n = self.n + 1
            self._const *= 1 / self.n

    def differentiate(self) -> None:
        """Differentiate the singularity function in-place."""
        if self.n <= 0:
            self.n = self.n - 1
        else:
            self._const *= self.n
            self.n = self.n - 1

    def derivative(self) -> "Singularity":
        """Copy this function and return its derivative."""
        diff = Singularity(self.a, self.n)  # make a copy
        diff.differentiate()
        return diff


# =========================================================================== #
#                                  Functions                                  #
# =========================================================================== #

def linear_spacing(
    start: float,
    end: float,
    num_points: int = 100,
    end_point: bool = True,
    ret_step: bool = False,
):
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
