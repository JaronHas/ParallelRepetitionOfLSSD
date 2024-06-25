# Running this file results in a text file containing all the vertices
# (extreme points) of the no-signalling polytope for three players and binary
# inputs and outputs. It uses a package called cdd (cddlib), which is a wrapper
# for a c++ package with the same name https://people.inf.ethz.ch/fukudak/cdd_home/.
# With this package we can change between representations of a convex polytope.

import cdd

def three_players():
    """
    This function does all the work for this file. We first create all the
    linear constraints that define the no-signalling polytope. We then convert
    that representation to the representation using extreme points and rays and
    save that to a file.

    The linear constraints Ax <= b (b-Ax >= 0) are stored in a matrix as
    follows: [b, -A]. We define the rows of the matrix one by one, starting with
    positivity constraints, then no-signalling constraints and finally
    constraints to ensure a valid conditional probability distribution.

    We have variables for each of the possible Q(x,y,z | a,b,c), that, together,
    define a no-signalling conditional probability distribution. The order in
    which they are stored/referenced is based on the value of the bitstring
    xyzabc, so Q(0,1,0 | 1,0,1) is the 22-nd variable (21 + 1) and corresponds
    to the 23-rd element in each row (since b is the first element).
    """

    # Firstly, we need that each of the variables is positive,
    # so we add the constraints x >= 0 for each x.
    positivity = []
    for i in range(2**6):
        rule = [0] * (2**6 + 1)
        rule[i+1] = 1

        positivity.append(rule.copy())

    matrix = cdd.Matrix(positivity)

    # Here we add the non signalling constraints:
    #  - sum_x Q(x,y,z | 0, b, c) = sum_x Q(x, y, z | 1, b, c) for all y,z,b,c.
    # Two sums that must be equal, so there difference must be 0.
    nosignalling_constraints = []
    for i in range(2**4):
        bitstring = '{0:04b}'.format(i)
        rule = [0]*(2**6 + 1)
        rule[int('0' + bitstring[0] + bitstring[1] + '0' +
                 bitstring[2] + bitstring[3], 2) + 1] = 1
        rule[int('1' + bitstring[0] + bitstring[1] + '0' +
                 bitstring[2] + bitstring[3], 2) + 1] = 1
        rule[int('0' + bitstring[0] + bitstring[1] + '1' +
                 bitstring[2] + bitstring[3], 2) + 1] = -1
        rule[int('1' + bitstring[0] + bitstring[1] + '1' +
                 bitstring[2] + bitstring[3], 2) + 1] = -1
        nosignalling_constraints.append(rule.copy())

    for i in range(2**4):
        bitstring = '{0:04b}'.format(i)
        rule = [0]*(2**6 + 1)
        rule[int(bitstring[0] + '0' + bitstring[1] +
                 bitstring[2] + '0' + bitstring[3], 2) + 1] = 1
        rule[int(bitstring[0] + '1' + bitstring[1] +
                 bitstring[2] + '0' + bitstring[3], 2) + 1] = 1
        rule[int(bitstring[0] + '0' + bitstring[1] +
                 bitstring[2] + '1' + bitstring[3], 2) + 1] = -1
        rule[int(bitstring[0] + '1' + bitstring[1] +
                 bitstring[2] + '1' + bitstring[3], 2) + 1] = -1
        nosignalling_constraints.append(rule.copy())

    for i in range(2**4):
        bitstring = '{0:04b}'.format(i)
        rule = [0]*(2**6 + 1)
        rule[int(bitstring[0] + bitstring[1] + '0' +
                 bitstring[2] + bitstring[3] + '0', 2) + 1] = 1
        rule[int(bitstring[0] + bitstring[1] + '1' +
                 bitstring[2] + bitstring[3] + '0', 2) + 1] = 1
        rule[int(bitstring[0] + bitstring[1] + '0' +
                 bitstring[2] + bitstring[3] + '1', 2) + 1] = -1
        rule[int(bitstring[0] + bitstring[1] + '1' +
                 bitstring[2] + bitstring[3] + '1', 2) + 1] = -1
        nosignalling_constraints.append(rule.copy())

    # These constraints are equality constraints, so linear = True.
    matrix.extend(nosignalling_constraints, linear=True)

    # We add the the constraints that make sure the values form a
    # conditional distribution:
    # - sum_x,y,z Q(x,y,z|a,b,c) = 1 for all a,b,c
    distribution_constraints = []
    for i in range(2**3):
        condition = '{0:03b}'.format(i)
        rule = [0] * (2**6 + 1)
        rule[0] = 1
        for j in range(2**3):
            outcome = '{0:03b}'.format(j)
            rule[int(outcome + condition, 2) + 1] = -1
        distribution_constraints.append(rule.copy())

    # These constraints are also equality constraints.
    matrix.extend(distribution_constraints, linear = True)

    # We tell cdd that the created matrix represents a polytope by inequalities.
    # canonicalize() gets rid of unnecessary constraints.
    matrix.rep_type = cdd.RepType.INEQUALITY
    matrix.canonicalize()

    # Here the matrix is now interpreted as a polyhedron representation and
    # the other representation is found and written to a file
    poly = cdd.Polyhedron(matrix)
    with open('three_player_vertices.txt', 'w') as f:
        f.write(str(poly.get_generators()))

if __name__ == "__main__":
    three_players()