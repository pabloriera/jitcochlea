# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 18:02:01 2016

@author: miles
"""
import numpy as np
import pylab as pl
from jitcochlea import Cochlea


C = Cochlea('basic')


spatial_parameters = ("d", "ww","wz")
inputs = ()
formula = {'x': 'y',
           'y': 'p - g',
           'z1': '-wz*z2-(z1*z1+z2*z2)*z1+alpha*x',
           'z2': 'wz*z1-(z1*z1+z2*z2)*z2',
           'g': 'ww*(x+z1) + d*y '}
           
fixed_parameters = ("alpha",)

C.setup(formula, spatial_parameters, fixed_parameters, inputs)
C.generate_code()
C.build()

#%%
         
data = {'fs': 100000.0, 
         'n_channels':600,
         'length': 0.035,
         'density': 1000,
         'height': 0.001, 
         'middle_ear': False,
         'mass': 0.03, 
         'fluid':1,
         'm0':1.0,
         'mef':10.0,
         'solver':2,
         'abs_tol':1e-4,
         'rel_tol':1e-4}
         
from scipy.signal import tukey


f0 = 1000.0
n_t = int(0.1*data['fs'])
t_signal = np.arange(n_t)/data['fs']
stimulus = 1*np.sin(2*np.pi*t_signal*f0)*tukey(n_t)
stimulus += 1*np.sin(2*np.pi*t_signal*5*f0)*tukey(n_t)

fmax = 20000.0
fmin = 100.0
ff = np.flipud( np.logspace(np.log10(fmin),np.log10(fmax),data['n_channels']))

Q = 4
w = 2*np.pi*ff
ww = w**2
d = w/Q

data['ww'] = ww
d = 10
data['wz'] = np.r_[w[d:],np.zeros(d)]
data['d'] = d
data['alpha'] = 5*0
         
tt, X_t = C.run(stimulus, data=data,  decimate = 1)
#%%
pl.figure(23)
#pl.clf()
pl.semilogy( np.sqrt(X_t[:-2,4::4]**2).mean(0))
pl.ylim(1e-3,1e7)
pl.figure(24)
pl.clf()
pl.imshow(X_t[:,4::4],cmap = pl.cm.seismic,aspect='auto')
#%%
pl.figure(25)
pl.clf()
pl.plot(X_t[-2,3::4])

