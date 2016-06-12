# JIT C++ Cochlea dynamical model

This module allows to build and run a dynamical model of the cochlea with 1-D fluid coupling.

The dynamic equations of the elements of the cochlear partition can be written in a C like format, and then the module builds and runs it.

```python
from jitcochlea import Cochlea,db2rms
from scipy.signal import tukey

C = Cochlea('basic')

formula = {'x': 'y',       					# basic oscillator equations with fluid pressure (p) and impedance term (g)
           'y': 'p - g',
           'g': 'ww*x + d*y '}   # the term g is mandatory as it is involved for solving the pressure p

spatial_parameters = ("d", "ww")       # the spatial parameters are set from the base to apex
fixed_parameters = ()

C.setup(formula, spatial_parameters, fixed_parameters)
C.generate_code()
C.build()

data = {'fs': 100000.0, 'n_channels':600,'decimate': 4}

fmax = 16000.0
fmin = 100.0
ff = np.flipud( np.logspace(np.log10(fmin),np.log10(fmax),data['n_channels']))

Q = 4
w = 2*np.pi*ff

data['ww'] =  w**2
data['d'] = w/Q

duration = 0.2 # seconds
f0 = 500.0 # hertz
n_t = int(duration*data['fs'])
t_signal = np.arange(n_t)/data['fs']
s0 = np.sin(2*np.pi*t_signal*f0)
stimulus = db2rms(40)*s0*tukey(n_t)

out = C.run(stimulus, data=data)        # the stimulus is the signal that forces the oval window, 
											# the data provides the values of the parameters, the cochlea dimensions, 
											# and the simulation configurations.
x = out['x']
```

**Dependencies:**

- Boost with odeint (v1.52 or more)
- numpy
- g++

**In ubuntu:**

```
sudo apt-get install libboost-all-dev python-numpy build-essential

sudo python setup.py install

sudo chmod 644 /usr/local/lib/python2.7/dist-packages/jitcochlea-1.0-py2.7.egg/src/*
```

**TODO**

Add noise, arbitrary couplings, time delayed feedback
