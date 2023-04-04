import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import random
import sys
import math

epsilon = 0.1
delta = 1
# r < epsilon/delta
r = 0.07
B = int(-1/r * np.log(1-(1-np.exp(r))/(1-np.exp(epsilon/delta))))
print("B: ",B)

# test_lower < test_upper
b1 = random.randint(-B, B)
b2 = random.randint(-B, B)
test_lower = b2
test_upper = b1
if b1 < b2:
    test_lower = b1
    test_upper = b2
# test_lower = 3
# test_upper = 17
print("test lower bound: ",test_lower)
print("test upper bound: ",test_upper)

def calculate_prob(lb, ub):
    sum = 0
    c = np.exp(epsilon/delta)
    coe = (c - 1)/(c + 1)
    #print("coe: ",coe)
    for i in range(lb, ub+1):
        sum += (coe * np.exp(-r * abs(i)))
    return sum

prob = calculate_prob(test_lower, test_upper)
print("total prob: ",prob)

def sampleGeometric(r):
    left = 0
    right = sys.maxsize
    while (left + 1 < right):
        mid = math.ceil((left - (math.log(0.5) + math.log1p(math.exp(r * (left - right)))) / r))
        mid = min(max(mid, left + 1), right - 1)
        q = math.expm1(r * (left - mid)) / math.expm1( r * (left - right))
        rnd = random.random()
        if (rnd <= q):
            right = mid
        else:
            left = mid

    return right

def sampleTwoSidedGeometric(r):
    geometricSample = 0
    sign = False
    while (geometricSample == 0 and (not sign)):
        geometricSample = sampleGeometric(r) - 1
        sign = random.choice([True, False])

    if sign:
        return geometricSample
    else:
        return -geometricSample

count = 0
n_samples = 1000000
sample_list = []
for i in tqdm(range(n_samples)):
    sample = sampleTwoSidedGeometric(r)
    while abs(sample) > B:
        sample = sampleTwoSidedGeometric(r)
    if sample >= test_lower and sample <= test_upper:
        count += 1
    sample_list.append(sample)

print("ratio: ",count/n_samples)

plt.hist(sample_list,bins=2*B+1,color='blue')
plt.show()

