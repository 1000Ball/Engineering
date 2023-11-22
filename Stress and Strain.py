'''Stress/strain relationships. Not intended to double check if all inputs have/don't have units '''

import numpy as np
from thermostate import Q_

## _______________________________________________________________________________________________________________

def stress(Force, CS_Area, L0=None, Delta_L=None, strain=None):
    '''Function that will calculate "Engineering stress" with values of force
    and cross-sectional area. If lengths are provided "True stress" can be
    calculated. All variables can be input as regular numbers with no units,
    or as a tuple/list formatted as (<quantity>, <units>), <units> being a string.'''

    if (type(Force) and type(CS_Area)) is (tuple or list):
        Force = Q_(*Force)
        CS_Area = Q_(*CS_Area)

    ## "Engineering stress" is sigma = F/A_0
    if (L0 or Delta_L or strain) is None:
        return (Force/CS_Area)

    ## "True stress" is sigma*(1+dL/L0)
    elif strain != None:
        if type(strain) is (tuple or list):
            strain = Q_(*strain)
        return ((Force/CS_Area)*(1+strain))
    
    else:
        try:
            if (type(L0) and type(Delta_L)) is (tuple or list):
                L0 = Q_(*L0)
                Delta_L = Q_(*Delta_L)
            return ((Force/CS_Area) * (1 + Delta_L/L0))
        except TypeError:
            print("Both L0 and Delta_L must have values if you're seeking True stress")
            return

## _______________________________________________________________________________________________________________

def strain(L0=None, L=None, A0=None, A=None, strain=None, output=None):
    '''Function that will calculate both "Engineering strain" and "True strain"
    with a set of lengths. Returns "True strain" unless specified.
    The 0 subscript indicates original length/area.'''

    if (type(L0) and type(L)) is (tuple or list):
        L0 = Q_(*L0)
        L = Q_(*L)
    if (type(A0) and type(A)) is (tuple or list):
        A0 = Q_(*A0)
        A = Q_(*A)

    ## "Engineering stress" is epsilon = Delta_L/L0
    keyword = 'engineering'
    if (type(output) is str) and (output.lower() == keyword):
        try:
            return ((L-L0)/L0)
        except TypeError:
            print("Need to enter values for L0 and/or L")
            return

    ## "Engineering stress" is epsilon_T = ln(L/L0) = ln(A0/A) = ln(1+epsilon)
    keyword = 'areas'
    if (type(output) is str) and (output.lower() == keyword):
        try:
            return (np.log(A0/A))
        except TypeError:
            print("Need to enter values for A0 and/or A")
            return

    if strain is None:
        try:
            return (np.log(L/L0))
        except TypeError:
            print("Need to enter values for L0 and/or L")
            return

    else:
        try:
            return (np.log(1+strain))
        except TypeError:
            print("Valid arguments for length, area, or strain must be passed")
            return
   

    
    
    
