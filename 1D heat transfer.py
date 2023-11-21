''' For solving one-dimensional steady state conduction with SymPy'''

import numpy as np
from sympy import *
from thermostate import Q_
import matplotlib.pyplot as plt

## Establishing symbols with SymPy
T, x, q, L, k = symbols('T, x, q, L, k')

## The characteristic equation:
T = Function('T')
Eq_0 = Eq(Derivative(T(x), x, x), -q/k)
Eq_0_sol = dsolve(Eq_0)

## Will produce two constants. Can define and rearrange for them as such:
C1, C2 = symbols('C1, C2')
C1_sol = solve(Eq_0_sol, C1)
C2_sol = solve(Eq_0_sol, C2)
Eq_C1 = Eq(C1, *C1_sol)
Eq_C1 = Eq(C1, *C1_sol)

## Boundary conditions
