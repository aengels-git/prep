import numpy as np
from functools import reduce

import sys
import inspect

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


def align_grid(*args):
    """
    Based on an arbirtary number of lists or numpy arrays
    tries to align the dimensions of all arrays, which requires that the dimensions of all arrays can be aligned 
    by repeatingly drawing and concatenating the smaller arrays  
    returns a numpy grid were each column has the same length
    """
    arg_size = [len(arg) for arg in args]
    repeats = list(map(lambda x: int(arg_size[np.argmax(arg_size)] / x), arg_size))
    equal_length_list = []
    for current_list, repetitions in zip(args, repeats):
        #print(np.repeat(current_list, repetitions))
        equal_length_list.append(np.repeat(current_list, repetitions))

    len_of_items = [len(arg) for arg in equal_length_list]
    assert all(i == len_of_items[0] for i in len_of_items), "Dimensions of ICD and ATC Settings should be a multiple of one another"
    return np.array(equal_length_list).reshape(len(args), len_of_items[0]).T


def ls(functions=False):
    imports = "os","re", "imports", "inspect","polars", "pandas", "sys", "numpy", "functions", "exit", "get_ipython", "In", "Path", "Union","quit", "seaborn"
    env_objects = [vars for vars, obj in inspect.getmembers(sys.modules[__name__]) if (vars.startswith("__") == 0 and vars.startswith("_") == 0 and vars not in imports and inspect.isfunction(eval(vars))==functions)]
    return env_objects
