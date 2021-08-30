# =========================================================================== #
#                                  utils.py                                   #
# =========================================================================== #

"""Utility objects for the 'potts' package"""

# =========================================================================== #
#                                  Functions                                  #
# =========================================================================== #


def sing(x, a, n):
    """Singularity function"""
    return 0 if x <= a else (x - a) ** n


def linear(start, end, num_points):
    step = (end - start) / num_points
    rv = [start]
    while len(rv) < num_points:
        rv.append(rv[-1] + step)
    rv.append(end)
    return rv
