import ctypes
from numpy.ctypeslib import ndpointer
import numpy as np
from string import Template

from .tools import DynLib, eqparser


class Cochlea():
    
    def __init__(self,name):
        self.name = name
        self.builded = False
    
    def setup(self, formula, spatial_parameters, fix_parameters, inputs):
        
        #spatial_parameters = ("d", "ww")
        #inputs = ()
        #formula = {'x': 'y','y': 'p - g','g': 'ww*x + d*y' }
        #fix_parameters = ()
        
        self.formula = formula
        self.spatial_parameters = spatial_parameters
        self.fix_parameters = fix_parameters
        self.inputs = inputs
            
        self.dynvars, self.g_assign, self.equation, self.n_vars, self.n_inputs, self.n_spatial_parameters, self.n_fix_parameters = eqparser(formula, spatial_parameters, fix_parameters, inputs)
        
        #dynvars,g_assign, main_eq, n_vars, n_inputs, n_spatial_parameters, n_fix_parameters = eqparser(formula, spatial_parameters, fix_parameters , inputs)
        #g_assign = "g[i] = X[i*n_vars+1] * pa[i+1*N] +  X[i*n_vars] * pa[i+0*N] ;"

        
        
    def generate_code(self,debug=False,dtype_=np.float64):        
        import os
        # print os.getcwd()
        installed_path = os.path.dirname(os.path.realpath(__file__))+'/'
        # print installed_path
        # os.chdir( os.path.dirname(os.path.realpath(__file__))  )
        # print os.getcwd()
        
        self.dtype = dtype_
        
        with  open(installed_path+"../src/jitcochlea.cpp",'r') as file_:
            self.code0 = file_.read()
        
        with  open(installed_path+"../src/cochlea.cpp",'r') as file_:
            self.code1 = file_.read()
        
        with  open(installed_path+"../src/cochlea.hpp",'r') as file_:
            self.code2 = file_.read()
                
        subs = {"system_equation_0":self.equation.replace("i","0").replace("j","0"),
                "system_equation_i":self.equation,
                "g_assignation": self.g_assign,
                "input_0": "linear_interpolation(in,t / dt)",
                "input_i": 0,
                "debug0":["//",""][debug]}        
                
        self.code1 = Template(self.code1).substitute(subs)

        
    def build(self,include_dirs_=[""]):
    
        include_dirs = ["../src/"]+include_dirs_
        
        self.lib = DynLib(self.name)
        self.lib.build_code([self.code0, self.code1],True, include_dirs = include_dirs)
        self.func = self.lib.get_function("run")
        
        self.builded = True
        
        #In the future this should be workedout automaticlay by DynLib
        f = ctypes.c_double
        pd = ndpointer(f, flags="C_CONTIGUOUS")
        i = ctypes.c_int
        pi = ndpointer(i, flags="C_CONTIGUOUS")        
        self.func.argtypes = [pd,pd,pd,pd,pd,pd,pd,pi,pd]

    def erase_lib(self):
        if self.builded: 
            del(self.lib)
        
    def __del__(self):
         
        self.erase_lib()
       
    def run(self, stimulus, X_0 = np.array([]), data={},  decimate = 1):
        import numpy as np
    
        #ff = np.flipud( np.logspace(np.log10(data['fmin']),np.log10(data['fmax']),data['n_channels']))
        #
        #w = 2*np.pi*ff
        #ww = w**2
        #dd = w/data['Q']
        
        #spatial_parameters = np.zeros( (self.n_spatial_parameters,n_channels)).astype(self.dtype)
        #spatial_parameters[0,:] = ww
        #spatial_parameters[1,:] = dd
        #
        #fix_parameters = np.array([]).astype(self.dtype)
        #inputs = np.array([]).astype(self.dtype)

        #X_0 = np.zeros( n_channels*self.n_vars ).astype(self.dtype)
        
        #from scipy.signal import tukey
        #f0 = 1000.0
        #t_signal = np.arange(n_t)/data['fs']
        #signal = np.sin(2*np.pi*t_signal*f0)*tukey(n_t)
        
        data_ = {'fs': 100000.0, 'height': 0.001, 
                'middle_ear': False, 'density': 1000, 'length': 0.035,
                'mass': 0.03, 'fmin': 100.0, 'fluid':1,
                'n_channels':400, 'm0':1,'mef':10.0,
                'solver':0,'abs_tol':1e-4,'rel_tol':1e-4}
                
        data_.update(data)
        data = data_.copy()        
        
        n_channels = data['n_channels']

        array_spatial_parameters = np.zeros( (self.n_spatial_parameters,n_channels)).astype(self.dtype)
        array_fix_parameters = np.zeros( self.n_fix_parameters )


        for i,k in enumerate(self.spatial_parameters):
            array_spatial_parameters[i,:]=data[k]
        
        for i,k in enumerate(self.fix_parameters):
            array_fix_parameters[i]=data[k]

        if X_0.size == 0:
            X_0 = np.zeros((n_channels*self.n_vars))
            

        n_t = stimulus.size
        dec = decimate
        n_t_dec = int(n_t/dec)
        fluid = data['fluid']
        
        dx = data['length']/data['n_channels']
               
        kappa = data['mass']*data['height']/2/data['density']
        alpha = kappa / dx / data['height']*data['mef']
        beta = dx / data['height']*data['mef']
        
        tt = np.zeros( (n_t_dec, 1) ).astype(self.dtype)
        X_t = np.zeros( (n_t_dec, n_channels*self.n_vars) ).astype(self.dtype)                        
       
        signal = data['mass']*np.convolve(stimulus,[1,-2,1],mode='same')*data['fs']**2
        inputs = np.array(signal).astype(self.dtype)
                  
        dimensions = np.array([n_t,self.n_vars,n_channels, self.n_inputs, self.n_spatial_parameters,self.n_fix_parameters, data['fs'], dec]).astype(np.int32)
        base_parameters = np.array([alpha, beta, data['m0'], fluid]).astype(self.dtype)
        solver_options = np.array([data['solver'], data['abs_tol'], data['rel_tol']]).astype(self.dtype)
        # extern "C" void run(floating* X_t, floating* tt, floating* inputs, floating* fix_parameters, floating* parameters, floating* base_parameters, int* dimensions, floating* solver_options )
        
        self.func( X_t, tt, X_0, inputs, array_fix_parameters, array_spatial_parameters, base_parameters, dimensions, solver_options )
        
        return tt,X_t