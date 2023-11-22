''' For solving one-dimensional steady state conduction with thermal generation via SymPy'''

import numpy as np
from sympy import *
import matplotlib.pyplot as plt

## Establishing symbols with SymPy
T, x, q_dot, L, k = symbols('T, x, q^dot, L, k')

## The characteristic equation:
T = Function('T')
Eq_0 = Eq(Derivative(T(x), x, x), -q_dot/k)
Eq_0_sol = dsolve(Eq_0)

## Will produce two constants. Can define and rearrange for them as such:
C1, C2 = symbols('C1, C2')
C1_sol = solve(Eq_0_sol, C1)
C2_sol = solve(Eq_0_sol, C2)
Eq_C1 = Eq(C1, *C1_sol)
Eq_C2 = Eq(C2, *C2_sol)

## SymPy can't handle tagged data from thermostate...
## Not ideal but solving ODE's is a nice feature
Length = float(input("What is the thickness of the wall? "))
Cond = float(input("What is the thermal conductivity of the wall? "))
T_s1 = float(input("What is the temperature at x=0? "))
T_s2 = float(input("What is the temperature at x=L? "))
q = float(input("What is the internal generation of the wall? "))
C1_c = Eq_C1.subs({x:0})
C1_c = C1_c.subs({T(0):T_s1})
C2_c = Eq_C2.subs({x:L, C1:C1_c.rhs})
C2_c = C2_c.subs({T(L):T_s2})
OneD_dict = {C1:C1_c.rhs, C2:C2_c.rhs, L:Length, k:Cond, q_dot:q}
Equation = Eq_0_sol.subs(OneD_dict)


x_domain = np.linspace(0, Length, 200)
lam_x = lambdify(x, Equation.rhs, modules=['numpy'])
plt.figure(figsize=(8,3))
plt.plot(x_domain, lam_x(x_domain))
plt.show()

## I don't plan to use SymPy like this again. Symbolic relationships are best for quick derivations and simplifications.
