# This file contains the necessary functions to find optimal classical winning
# probabilities.

import numpy as np
import itertools as it
from example1 import distribution_matrix_n

def find_win_prob_example1_dist(f, g, distribution, n):
    """
    This function calculates the winning probability of a deterministic strategy
    given by two functions f and g.
    """
    N = 2**n
    prob = 0
    for (x,a,b) in it.product(np.arange(N), repeat=3):
        if f[a] == g[b] == x:
            prob += distribution[x][a][b]
    return prob

def find_max_win_prob(alpha, n):
    """
    This function loops over all possible deterministic strategies to find
    the optimal classical winning probability.
    """
    N = 2**n
    dist = distribution_matrix_n(alpha, n)

    max_win_prob = 0
    for f in it.product(np.arange(N), repeat=N):
        win_prob = find_win_prob_example1_dist(f, f, dist, n)
        if win_prob > max_win_prob:
            max_win_prob = win_prob
            # print(f, win_prob)
    return max_win_prob

if __name__ == "__main__":
    print(find_max_win_prob(0.328, 2))