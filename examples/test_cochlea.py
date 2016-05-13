# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 18:02:01 2016

@author: miles
"""
import numpy as np
import pylab as pl
from jitcochlea import Cochlea


C = Cochlea('basic')


spatial_parameters = ("d","d0", "ww")
inputs = ()
formula = {'x': 'y',
           'y': 'p - g',
           'g': 'ww*x+ d*y + d0*x*x*y '}
fixed_parameters = ()

C.setup(formula, spatial_parameters, fixed_parameters, inputs)
C.generate_code()
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
         'rel_tol':1e-4}
         
from scipy.signal import tukey

f0 = 500.0
n_t = int(0.2*data['fs'])
t_signal = np.arange(n_t)/data['fs']
stimulus = 1000*np.sin(2*np.pi*t_signal*f0)*tukey(n_t)

x = np.linspace(0,data['length'],data['n_channels'])

fmax = 16000.0
fmin = 100.0
ff = np.flipud( np.logspace(np.log10(fmin),np.log10(fmax),data['n_channels']))

Q = 60
w = 2*np.pi*ff
ww = w**2
d = w/Q

data['ww'] = ww
data['d'] = d
data['d0'] = d*10.0
         
tt, X_t = C.run(stimulus, data=data,  decimate = 1)
#%%
pl.semilogy(x[1:], np.sqrt(X_t[:-1,2::2]**2).mean(0))
