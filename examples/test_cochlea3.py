# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 18:02:01 2016

@author: miles
"""
import numpy as np
import pylab as pl
from jitcochlea import Cochlea,db2rms


C = Cochlea('basic')

spatial_parameters = ("d","d0", "ww","a","b","s")
inputs = ()
formula = {'x': 'y',
           'y': 'p - g',
           'g': 'ww*x+ d*y + d0*x*x*y + ww*(a*x[s] + b*x[-s])'}
fixed_parameters = ()

C.setup(formula, spatial_parameters, fixed_parameters, inputs)
C.generate_code(debug=False)
C.build()

#%%
         
data = {'fs': 100000.0, 
         'n_channels':800,
         'length': 0.035,
         'density': 1000,
         'height': 0.001, 
         'middle_ear': False,
         'mass': 0.03, 
         'fluid':1,
         'm0':1,
         'mef':1,
         'solver':0,
         'abs_tol':1e-4,
         'rel_tol':1e-4,
         'decimate':1}
         
from scipy.signal import tukey

f0 = 1000.0
n_t = int(0.3*data['fs'])
t_signal = np.arange(n_t)/data['fs']
stimulus = db2rms(40)*np.sin(2*np.pi*t_signal*f0)*tukey(n_t)

x = np.linspace(0,data['length'],data['n_channels'])

fmax = 16000.0
fmin = 100.0
ff = np.flipud( np.logspace(np.log10(fmin),np.log10(fmax),data['n_channels']) )

Q = 4
w = 2*np.pi*ff
ww = w**2
d = w/Q

data['ww'] = ww
data['d'] = d
data['d0'] = d*1e12
data['a'] = 0.15
data['b'] = -0.15
data['s'] = 0.004
         
tt, X_t =C.run(stimulus, data=data)

print "NANS", isnan(X_t).sum()
#%%

pl.semilogy(x[1:], np.sqrt(X_t[:-1,2::2]**2).mean(0))
