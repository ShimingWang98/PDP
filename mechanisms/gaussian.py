import numpy as np
from mechanisms.abstract import Mechanism
import time
import math

def _identity(x):
    return x.item(0)

class GaussianMechanism(Mechanism):

    def __init__(self, fun=_identity, var: float = 0):
        """
        Create a Gaussian mechanism.

        Args:
            fun: The function performed before adding noise. The function must accept a 1d array and produce a scalar.
            var: The variance of the Gaussian noise
        """
        self.fun = fun

        # to get the same utility of the laplace mechanism, we directly give the variance
        self.var = var

    def m(self, a, n_samples: int = 1):
        loc = self.fun(a)
        return np.random.normal(loc=loc, scale=math.sqrt(self.var), size=n_samples)
