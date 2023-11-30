import numpy as np
from thermostate import Q_  #Here so user does not need to import when initiated
import matplotlib.pyplot as plt

'''Formula pertaining to the beding of a cantilever beam
with a concentrated load P at any point'''

#-----------------------------------------------------------------------------

def Cantilever_Concentrated(P, a, L, E, I):
    '''P: Concentrated load, a: Location of load, L: Beam length,
    E: Young's modulus, I: Second momt of inertia
    
    Calculating values of slope at free end, max deflection, as well as
    the profile of the beam'''

    ## Solving for the remainder of the beam's length
    b = L-a

    ## Slope
    theta = ((P * a**2) / (2*E*I)).to('degrees')

    ## Max deflection
    delta_max = ((P * a**2) / (6*E*I) * (3*L-a)).to('mm')

    ## Profile relationships, ~400 points total
    n = 400
    a_ratio = a/L
    b_ratio = b/L
    a_points = int((a_ratio*n).round(0))
    b_points = int((b_ratio*n).round(0))

    x = []
    y = []
    x1 = np.linspace(0, a, a_points)
    up_to_a = lambda x: ((P*x**2) * (3*a-x) / (6*E*I)).to('mm')
    for i in x1:
        x.append(i)
        y.append(up_to_a(i))

    x2 = np.linspace(a, L, b_points)
    a_to_L = lambda x: ((P*a**2) * (3*x-a) / (6*E*I)).to('mm')
    for i in x2:
        x.append(i)
        y.append(a_to_L(i))

    return {'Slope': theta, 'Max deflection': delta_max, 'Profile': (x,y)}

#-----------------------------------------------------------------------------

def plot_it(Profile, x_units = None, y_units = None):
    '''Using the result from the previous function to plot a profile curve. Can specify axis units'''
    
    x = Profile[0][:]
    y = Profile[1][:]

    if x_units != None:
        for i,j in enumerate(x):
            x[i] = x[i].to(x_units).magnitude
    else:
        x_units = x[0].units
        for i,j in enumerate(x):
            x[i] = j.magnitude



    if y_units != None:
        for i,j in enumerate(y):
            y[i] = y[i].to(y_units).magnitude
    else:
        y_units = y[0].units
        for i,j in enumerate(y):
            y[i] = j.magnitude

    plt.figure(figsize=(8,4))
    plt.plot(x,y)
    plt.title('Cantilever beam deflection profile')
    plt.xlabel(f'Distance along beam [{x_units}]')
    plt.ylabel(f'Deflection of beam [{y_units}]')
    plt.show()
#-----------------------------------------------------------------------------

if __name__ == "__main__":
    ## Outrageous test case just to see if units work out and all
    E,L,I,P,a =Q_(-360, 'GPa'),Q_(20, 'm'),Q_(16/12, 'in^4'),Q_(400, 'N'),Q_(12, 'm')

