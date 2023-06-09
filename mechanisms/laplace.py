import numpy as np
from mechanisms.abstract import Mechanism
import time
from sample.sample_laplace import *

def _identity(x):
    return x.item(0)


class LaplaceMechanism(Mechanism):

    def __init__(self, original=True, fun=_identity, eps: float = 5.0, r=2.0, c=0.05 ):
        """
        Create a Laplace mechanism.

        Args:
            fun: The function performed before adding noise. The function must accept a 1d array and produce a scalar.
            eps: target epsilon
            r: parameter in practical differential privacy, decided by eps and c
            c: if eps and r are given, no need to assign c anymore
        """
        self.fun = fun
        self.scale = 1.0 / eps
        # use original laplace or practical laplace
        self.original = original
        # r will change according to c and eps
        self.r = r

    def m(self, a, n_samples: int = 1):
        # original laplace
        if self.original:
            loc = self.fun(a)
            return np.random.laplace(loc=loc, scale=self.scale, size=n_samples)
        # practical laplace
        else:
            loc = self.fun(a)
            result = practical_continuous_laplace(b=self.scale, r=self.r, size = n_samples)
            result += loc
            return result

    # uniform distribution
    # def m(self, a, n_samples: int =1):
    #     loc = self.fun(a)
    #     result = np.random.uniform(low=-self.scale, high=self.scale, size=n_samples)
    #     return result+loc

    def test_utility(self, n_samples=1000000):
        if self.original:
            noise = np.random.laplace(scale=self.scale, size=n_samples)
        else:
            noise = practical_continuous_laplace(b=self.scale, r=self.r, size=n_samples)
        # noise between [-0.1, 0.1]
        truncated_noise = noise[np.where(abs(noise) <= 0.1)]
        # the ratio of noise between [-0.1, 0.1]
        ratio = len(truncated_noise)/n_samples
        print("truncated ratio: ",ratio)
        # variance of noise
        var = np.var(noise)
        print("utility: ",var)
        return var



if __name__ == '__main__':
    mechanism = LaplaceMechanism()
    n_samples = 1000000
    mechanism.test_utility(n_samples)