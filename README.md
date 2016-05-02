<H2>Cochlea dynamical model</H2>

This module allows to build and run a dynamical model of the cochlea with 1-D fluid coupling.

The dynamic equations of the elements of the cochlear partition can be written in a C like format, and then the module builds and runs it.

```python
C = Cochlea('basic')

formula = {'x': 'y',       					# basic oscillator equations with fluid pressure (p) and impedance term (g)
           'y': 'p - g',
           'g': 'ww*x + d*y + d0*x*x*y '}   # the term g is mandatory as it is involved for solving the pressure p

spatial_parameters = ("d","d0", "ww")       # the spatial parameters are set from the base to apex
inputs = ()								    # inputs are time dependent signals

fixed_parameters = ()

C.setup(formula, spatial_parameters, fixed_parameters, inputs)
C.generate_code()
C.build()

tt, X_t = C.run(stimulus, data=data)        # the stimulus is the signal that forces the oval window
```

**TODO**

Add noise, arbitrary couplings, feedback, lateral feed, fix setup

**Dependencies:**

- Boost with odeint (starting in v 1.52)
- numpy
- g++

**In ubuntu:**

```
sudo apt-get install libboost-all-dev python-numpy build-essential
```

**Installation:**

```
sudo python setup.py install
sudo chmod 644 /usr/local/lib/python2.7/dist-packages/jitcochlea-1.0-py2.7.egg/src/*
```
