# Running this file creates 2 files: one with all relevant no-signalling
# strategies, according to corollary 4.1, and one with all relevant deterministic
# strategies, according to lemma 4.1. The deterministic strategies in this file
# are also described by a conditional distribution instead of 3 binary functions.

from fractions import Fraction
import itertools as it
import numpy as np

def is_relevant_three_player(strategy):
    """
    This function checks whether a given no-signalling strategy is relevant
    according to corollary 4.1 (we have d = 2), by checking if there
    exist x,a,b,c in {0,1} such that Q(x,x,x|a,b,c) > 1/2. (We use the same
    ordering as for finding polytope extrema.)
    """
    for j in range(2**3):
        bitstring = '{0:03b}'.format(j)
        value1 = Fraction(strategy[int('000' + bitstring, 2)])
        value2 = Fraction(strategy[int('111' + bitstring, 2)])
        if value1 > Fraction(1,2) or value2 > Fraction(1,2):
            return True

    return False

def filter_three_players():
    """
    This reads all the no-signalling strategies at the vertices of the
    no-signalling polytope from a file and filters out the strategies that
    are not relevant. The remaining strategies are written to another file.
    (This file then also contains some deterministic strategies, but that is
    okay)
    """
    all_relevant_strats = []
    with open("three_player_vertices.txt") as strategies:
        for i, line in enumerate(strategies):
            # We skip the first 2 and last line, since they contain
            # irrelevant information.
            if i >= 3 and line != "end":
                # We skip the first 2 characters, since they say whether
                # or not that line is a vertex or ray.
                # They should all be vertices.
                line_split = line[3:len(line) - 1].split(" ")
                if is_relevant_three_player(line_split):
                    all_relevant_strats.append(line_split)
    write_to_file(all_relevant_strats,
                  "three_player_all_relevant_strats.txt")

def strat_to_Q(f, g, h):
    """
    This function takes a strategy defined by three deterministic
    functions f, g and h and converts it into a strategy defined by a
    conditional distribution Q.
    """
    Q = np.zeros((2**6), dtype=int)
    for (x,y,z,a,b,c) in it.product([0,1], repeat=6):
        if f[a] == x and g[b] == y and h[c] == z:
            # Again, we order the Q(x,y,z|a,b,c) according to the value of
            # the bitstring xyzabc.
            Q[x*(2**5) + y*(2**4) + z*(2**3) + a*(2**2) + b*2 + c] = 1

    return Q

def relevant_det_strats_three_player_binary():
    """
    This function generates all relevant deterministic strategies according
    to lemma 4.1 (which can be summarized by: the output sets need to be equal).
    """
    strats = []
    for (f,g,h) in it.product(it.product([0,1], repeat=2), repeat=3):
        if set(f) == set(g) == set(h):
            strats.append(list(map(str, strat_to_Q(f,g,h))))

    write_to_file(strats, "relevant_det_strats.txt")

def write_to_file(strategy_list, file_name):
    """
    This function takes a list of strategies and writes them to a file.
    """
    for i in range(len(strategy_list)):
        strategy_list[i] = " ".join(strategy_list[i])
    to_file = "\n".join(strategy_list)
    with open(file_name, 'w') as f:
        f.write(to_file)

if __name__ == "__main__":
    filter_three_players()
    relevant_det_strats_three_player_binary()