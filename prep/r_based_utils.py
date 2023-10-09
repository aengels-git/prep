import numpy as np
from functools import reduce
def expand_grid(*args):
    """
    Based on an arbirtary number of lists or numpy arrays 
    returns a numpy grid of all possible combinations of the elements of these lists or arrays
    """
    liste = [len(arg) for arg in args]
    n_comb = reduce(lambda x, y: x * y,liste)
    X = np.array(
        np.meshgrid(*args)
    ).reshape(len(args),n_comb).T
    return X