# This file will give the largest gap possible for three player binary LSSD.
# It does this by solving multiple LP's that try to maximize the gap between
# the no-signalling and classical winning probabilities over the set of all
# probability distributions. Each of the LP's has variables that define a
# probability distribution and two extra variables that represent the best
# classical and best no-signalling winning probabilities. These two variables
# must satisfy constraints that they are higher than the winning probabilities
# of the strategies in the files containing relevant strategies. However, we
# need an upperbound for the variable that represents the best no-signalling
# winning probability, since otherwise the LP would be unbounded. This is why
# we solve multiple LP's: each time we set the no-signalling variable to be
# equal to the no-signalling winning probability of a strategy (which is the
# same as assuming that this strategy would be the best strategy).

from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable, PULP_CBC_CMD
from fractions import Fraction

def three_player_binary_LP_pulp(det_strats, ns_strats, set_to_equality):
    """
    This function solves an LP that finds the largest gap between
    no-signalling and classical strategies, assuming that the strategy
    referenced by set_to_equality is the best no-signalling strategy.
    """
    model = LpProblem(name="max_gap_3player_bin", sense=LpMaximize)

    # We have a variable for each P(x,a,b,c), so 2^4 variables, which we order
    # by the value of the bitstring xabc.
    variables = []
    for i in range(2**4):
        variables.append(LpVariable(name='{0:04b}'.format(i), lowBound = 0))

    # These two variables represent the best classical and no-signalling
    # winning probabilities.
    max_det = LpVariable(name='maxdet', lowBound=0)
    max_ns = LpVariable(name='maxns', lowBound=0)

    # This constraint ensures that the variables form a valid probability
    # distribution
    model += (sum([variable for variable in variables]) == 1)

    # These constraints make sure max_det is higher than the winning
    # probabilities of each of the strategies in det_strats.
    # The winning probability of a strategy is given by:
    #  - sum_x,a,b,c Q(x,x,x|a,b,c)*P(x,a,b,c)
    for strategy in det_strats:
        # We loop over all bitstrings xabc and calculate the sum above.
        model += (max_det -
                  sum([strategy[int('{0:04b}'.format(i)[0]*3 +
                                    '{0:04b}'.format(i)[1] +
                                    '{0:04b}'.format(i)[2] +
                                    '{0:04b}'.format(i)[3], 2)] *
                       variables[int('{0:04b}'.format(i), 2)]
                       for i in range(2**4)]) >= 0)

    # These constraints make sure max_ns is higher than the winning
    # probabilities of each of the strategies in ns_strats. There is one
    # equality constraint that makes sure that max_ns is equal to the specified
    # no-signalling strategy.
    for j, strategy in enumerate(ns_strats):
        if j == set_to_equality:
            model += (max_ns -
                      sum([strategy[int('{0:04b}'.format(i)[0]*3 +
                                        '{0:04b}'.format(i)[1] +
                                        '{0:04b}'.format(i)[2] +
                                        '{0:04b}'.format(i)[3], 2)] *
                           variables[int('{0:04b}'.format(i), 2)]
                           for i in range(2**4)]) == 0)
        else:
            model += (max_ns -
                      sum([strategy[int('{0:04b}'.format(i)[0]*3 +
                                        '{0:04b}'.format(i)[1] +
                                        '{0:04b}'.format(i)[2] +
                                        '{0:04b}'.format(i)[3], 2)] *
                            variables[int('{0:04b}'.format(i), 2)]
                            for i in range(2**4)]) >= 0)

    # This constraint makes sure that whenever deterministic strategies are
    # strictly better that non-deterministic strategies, the LP has no solution.
    model += (max_ns - max_det >= 0)

    # The objective is to maximize the gap
    obj_func = max_ns - max_det
    model += obj_func

    model.solve(PULP_CBC_CMD(msg=0))
    print(f"Solution status: {LpStatus[model.status]}, gap:, {model.objective.value()}")
    # If no solution was found, model.objective.value() is 0, so that causes no
    # problems.
    return model.objective.value()

def read_strategies_from_file(file):
    """
    This function reads strategies from a file and stores them in a list.
    """
    strategies = []
    with open(file) as f:
        for line in f:
            strategy = list(map(Fraction, line.split(" ")))
            strategies.append(strategy)

    return strategies

def max_gap_three_player_binary():
    """
    This function loops over all relevant no-signalling strategies and
    solves calls three_player_binary_pulp() to solve the LP's with
    specific constraints set to equality.
    """
    det_strats = read_strategies_from_file("relevant_det_strats.txt")
    ns_strats = read_strategies_from_file(
                "three_player_all_relevant_strats.txt")

    max_gap = 0
    for i in range(len(ns_strats)):
        gap = three_player_binary_LP_pulp(det_strats, ns_strats, i)
        if gap > max_gap:
            max_gap = gap

    return max_gap

if __name__ == "__main__":
    print("Largest gap:", max_gap_three_player_binary())