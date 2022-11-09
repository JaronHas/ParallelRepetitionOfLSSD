#Importing necessary things for the program

import math
import cmath
from math import cos, pi, acos, floor, exp, sin, sqrt
import numpy as np
import mosek
import matplotlib.pyplot as plt
from sympy.core import S, expand
from ncpol2sdpa import *
import csv
import itertools as it
import operator as op

#Setting the 1st level of the NPA hierarchy
level = 1

#We define the projectors
A_configuration = [5]*4
B_configuration = [5]*4
A = generate_measurements(A_configuration, 'A')
B = generate_measurements(B_configuration, 'B')
monomial_substitutions = projective_measurement_constraints(A, B)

#To make it computationally efficient, taking into account that we work with projectors, we consider one of the projectors the identity minus the others
def mVar(mList, i):
    nOutcomes = len(mList)+1
    if i == nOutcomes-1:
        return S.One - sum(mList[j] for j in range(nOutcomes-1))
    else:
        return mList[i]

#We create an empty list where we are going to store the solutions  
r = []

#We solve it for different values of alpha
for alpha in np.arange(0.26,0.37,0.002):
    #We describe the input's probability
    def p(y):
        if y==1:
            return alpha
        if y==0:
            return 1-alpha
    
    def pr(x,y,z):
        if x==0:
            return 1/2*p(y)*p(z)
        if x==1:
            return 1/2*p(1-y)*p(1-z)
    
    def prob(x1,x2,y1,y2,z1,z2):
        return pr(x1,y1,z1)*pr(x2,y2,z2)
        
    #We describe the objective function
    objective = S.Zero      
    for x1,s1,t1,x2,s2,t2 in it.product(range(2), repeat = 6):
        objective=objective+prob(x1,x2,s1,s2,t1,t2)*mVar(A[2*s1+s2], 2*x1+x2)*mVar(B[2*t1+t2],2*x1+x2)
                         
                    
    objective = -expand(objective)
    sdp = SdpRelaxation(flatten([A, B]), verbose=0)
    
    #We add the `AB' in the `1+AB' level of the NPA hierarchy
    AB=[Ai*Bj for Ai in flatten(A) for Bj in flatten(B)]
  
    sdp.get_relaxation(level, objective=objective,
                                         substitutions=monomial_substitutions,
                                         extramonomials=AB)
    #We solve the SDP       
    sdp.solve(solver='mosek')
    #We store the solution together with its corresponding value of alpha
    r.append((alpha, -sdp.primal))
    print((alpha, -sdp.primal))
print(r)    
