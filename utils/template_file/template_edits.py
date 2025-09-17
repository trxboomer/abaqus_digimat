import numpy as np
import numpy.typing as npt


def vf_array(fiber_void_array: list[list[np.float64]]):
    
    """Creates a list of lists that contains the matrix, fiber and void volume fractions for a given test

    Returns:
        list[list[np.float64]]: each sublist contains the matrix, fiber and void volume fractions for a given test
    """
    result: list[list[np.float64]] = []
    for arr in fiber_void_array:
        if any(x < 1 for x in arr):
            continue
        

        else:
            result.append([1 - np.sum(fiber_void_array), arr[0], arr[1]])
            
    return result

def 
