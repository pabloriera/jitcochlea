<H2>Cochlea dynamical model</H2>

This module allows to build and run a dynamical model of the cochlea with 1-D fluid coupling.

The dynamic equations of the elements of the cochlear partition can be written in a C like format, and then the module builds and runs it.

```python
C = Cochlea('basic')

spatial_parameters = ("d","d0", "ww")
inputs = ()
formula = {'x': 'y',
           'y': 'p - g',
           'g': 'ww*x + d*y + d0*x*x*y '}
fixed_parameters = ()

C.setup(formula, spatial_parameters, fixed_parameters, inputs)
C.generate_code()
C.build()

tt, X_t = C.run(stimulus, data=data)
```


**Dependencies:**

Boost with odeint (starting in v 1.52)
numpy
g++

**In ubuntu:**

sudo apt-get install libboost-all-dev

**Installation:**

sudo python setup.py install

