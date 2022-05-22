# This file contains the necessary function(s) to do experiments with.

import matplotlib.pyplot as plt
import numpy as np
import math

def distribution_matrix_n(alpha, n):
    """
    This function creates a matrix consisting of all the values of P(x,a,b)
    for a specific alpha and number of simultaneous games n.
    (distribution[x][a][b] contains the value P(x,a,b).)
    Note that we have P(x,a,b) = P(x)P(a|x)P(b|x)
    """

    N = 2**n
    distribution = np.zeros((N,N,N))
    for output in range(N):
        for input1 in range(N):
            for input2 in range(N):
                # x is chosen uniformly so P(x) = 1/N.
                value = 1/N
                # Here we calculate P(a|x) and P(b|x), these probabilities
                # only depend on the number of differences between the
                # bitstrings x,a resp. x,b (so the number of ones in x^a
                # resp x^b)
                for thing in [input1, input2]:
                    difference = '{0:b}'.format(thing ^ output)
                    ones = 0
                    for bit in difference:
                        if bit =='1':
                            ones += 1
                    # here we multiply by P(a|x) resp. P(b|x)
                    value *= alpha**ones * (1-alpha)**(n-ones)
                distribution[output][input1][input2] = value
    return distribution

def create_graph(n, start, stop, step, nosignalling=True, classical=True):
    """
    This function finds the best nosignalling and classical winning
    probabilities for a range of alphas and plots them in a graph.
    """
    from classical import find_max_win_prob
    from nosignalling import ncopies

    alphas = np.arange(start, stop, step)
    ns_probs = []
    cl_probs = []
    for alpha in alphas:
        ns_probs.append(ncopies(alpha, n))
        cl_probs.append(find_max_win_prob(alpha, n))
    if classical:
        plt.plot(alphas, cl_probs, color='b')
    if nosignalling:
        plt.plot(alphas, ns_probs, color='r')

    plt.show()

if __name__ == "__main__":
    create_graph(2, 0, 0.5, 0.01)