""" minimize_interface.py

"""

from commonfunctions import * # common function
from lmfit import minimize, Parameters, Parameter, report_fit
import numpy as np


# create data to be fitted

data = (5. * np.sin(2 * x - 0.1) * np.exp(-x*x*0.025) +
        np.random.normal(size=len(x), scale=0.2) )

# define objective function: returns the array to be minimized
def fcn2min(paramdic, x, data, datadic, extrakeys,  extrakeyssolv):
    
    
    """ model decaying sine wave, subtract data"""
    amp = params['amp'].value
    shift = params['shift'].value
    omega = params['omega'].value
    decay = params['decay'].value

    model = amp * np.sin(x * omega + shift) * np.exp(-x*x*decay)
    
 
    
    totalerror, mae, rmse, bias, r2, slope, intercept, datadic = calc_error("0000", paramdic, datadic, extrakeys, extrakeyssolv + " RSOLV=% .3f" % (rsolvtest), outfile, nptype, yrel)
    
    return totalerror

# create a set of Parameters
params = Parameters()
params.add('amp',   value= 10,  min=0)
params.add('decay', value= 0.1)
params.add('shift', value= 0.0, min=-np.pi/2., max=np.pi/2)
params.add('omega', value= 3.0)


# do fit, here with leastsq model
result = minimize(fcn2min, params, args=(x, data))

# calculate final result
final = data + result.residual

# write error report
report_fit(params)

# try to plot results
try:
    import pylab
    pylab.plot(x, data, 'k+')
    pylab.plot(x, final, 'r')
    pylab.show()
except:
    pass
