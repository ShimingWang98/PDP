import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import math
from sympy import *
import sympy


# def practical_continuous_laplace(b, r, size):
#     ratio = math.ceil(1.0/(b * r) * 1.1)
#     scale = 1.0/r
#     B = -scale * np.log(1 - (b * r ))
#     n_samples = size[0]
#     tmp = list(size)
#     tmp[0] *= ratio
#     new_size = tuple(tmp)
#     result = np.random.laplace(scale=scale, size=new_size)
#     new_result = np.zeros((size))
#     for i in range(size[1]):
#         new_result[:,i] = result[:,i][np.where(abs(result[:,i]) <= B)][:n_samples]
#     assert (len(new_result) == n_samples)
#
#     return new_result

def practical_continuous_laplace(b, r, size):
    n_samples = size
    ratio = math.ceil(1.0/(b * r) * 1.1)
    scale = 1.0/r
    B = -scale * np.log(1 - (b * r ))
    result = np.random.laplace(scale=scale, size=ratio*n_samples)
    result = result[np.where(abs(result) <= B)][:n_samples]
    assert (len(result) == n_samples)

    return result