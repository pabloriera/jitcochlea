# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 18:02:01 2016

@author: miles
"""
import numpy as np
import pylab as pl
from jitcochlea import Cochlea,db2rms


C = Cochlea('basic')

spatial_parameters = ("d", "ww")

formula = {'x': 'y',
           'y': '- p - g',
           'g': 'ww*x+ d*y'}
fixed_parameters = ()

C.setup(formula, spatial_parameters, fixed_parameters)
C.generate_code()
C.build()

#%%
         
data = {'fs': 100000.0, 
         'n_channels':600,
         'length': 0.035,
         'density': 1000,
         'height': 0.001, 
         'mass': 0.5, 
         'fluid':1,
         'mef':1,
         'solver':0,
         'abs_tol':1e-4,
         'rel_tol':1e-4,
         'decimate':5}
         
from scipy.signal import tukey

f0 = 500.0
n_t = int(0.2*data['fs'])
t_signal = np.arange(n_t)/data['fs']
s0 = np.sin(2*np.pi*t_signal*f0)+np.sin(2*np.pi*t_signal*f0*4)
stimulus = db2rms(40)*s0*tukey(n_t)

x = np.linspace(0,data['length'],data['n_channels'])

fmax = 16000.0
fmin = 100.0
ff = np.flipud( np.logspace(np.log10(fmin),np.log10(fmax),data['n_channels']) )

Q = 5
w = 2*np.pi*ff
ww = w**2
d = w/Q

data['ww'] = ww
data['d'] = d

data['d0'] = d*10.0*0


re = C.run(stimulus, data=data)
xx = re['x']

pl.semilogy(x[:], np.sqrt(xx**2).mean(0))
