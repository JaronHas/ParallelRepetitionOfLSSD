# This file contains the function that can find the optimal no-signalling
# winning probability. It does this by solving an LP.

import numpy as np
import itertools as it
from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable, PULP_CBC_CMD
from example1 import distribution_matrix_n

def ncopies(alpha, n, show=False, show_image=False):
    N = 2**n
    distribution = distribution_matrix_n(alpha, n)

    model = LpProblem(name="ncopiy_no-signalling_strat", sense=LpMaximize)

    # We have a variable for each Q(x,y|a,b) and they should all be positive.
    variables = []
    for (output1, output2, input1, input2) in it.product(np.arange(N), repeat=4):
        variables.append(LpVariable(name=f"{output1},{output2}|{input1},{input2}", lowBound = 0))

    # We add the no-signalling constraints:
    #  - sum_x Q(x,y|a,b) = sum_x Q(x,y|a',b) for all y,a,a',b.
    # This is equivalent to
    #  - sum_x Q(x,y|0,b) = sum_x Q(x,y|a,b) for all y,a,b.
    for (output2, input2) in it.product(np.arange(N), repeat=2):
        for input1 in np.arange(1, N):
            model += (sum([variables[output1*(N**3) + output2*(N**2) + input2] for output1 in range(N)]) -
                      sum([variables[output1*(N**3) + output2*(N**2) + input1*N + input2] for output1 in range(N)]) == 0)

    for (output1, input1) in it.product(np.arange(N), repeat=2):
        for input2 in np.arange(1, N):
            model += (sum([variables[output1*(N**3) + output2*(N**2) + input1*N] for output2 in range(N)]) -
                      sum([variables[output1*(N**3) + output2*(N**2) + input1*N + input2] for output2 in range(N)]) == 0)

    # We add the constraints that make sure the variables form a valid
    # conditional distribution.
    for (input1, input2) in it.product(np.arange(N), repeat=2):
        model += (sum([variables[output1*(N**3) + output2*(N**2) + input1*N + input2] for (output1, output2) in it.product(np.arange(N), repeat=2)]) == 1)

    # the objective function is the winning probability of a strategy:
    # sum_x,a,b P(x,a,b) Q(x,x|a,b)
    obj_func = sum([distribution[output][input1][input2]*variables[output*(N**3) + output*(N**2) + input1*N + input2] for (output, input1, input2) in it.product(np.arange(N), repeat=3)])

    model += obj_func

    model.solve(PULP_CBC_CMD(msg=0))

    # some options to show for testing.
    if show:
        for var in model.variables():
            print(f"{var.name}: {var.value()}")
        print(model.objective.value())

    if show_image:
        new_array = np.zeros((N**2, N**2))
        for inputs in range(N**2):
            for outputs in range(N**2):
                new_array[inputs][outputs] = variables[outputs*(N**2) + inputs].value()
                if variables[outputs*(N**2) + inputs].value()==1:
                    print(variables[outputs*(N**2) + inputs].name)

        with open(f'{n}_game_ns_strats.txt', 'w') as f:
            text = ""
            for row in new_array:
                line = ""
                for element in row:
                    line += str(element) + " "
                text += line + "\n"
            f.write(text)

        for line in new_array:
            print(line)
        plt.imshow(np.transpose(new_array), interpolation="none")
        plt.show()

    return model.objective.value()

if __name__ == "__main__":
    print(ncopies(0.328, 2))