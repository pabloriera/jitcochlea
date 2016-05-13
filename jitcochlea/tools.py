import tempfile, os
from random import randint

class DynLib():


    def __init__(self,mod_name):
        self.mod_name = mod_name
        self.counter = 0
        self.builded_once = False
        

    def build_code(self,codes_list, clean=True , include_dirs = "[]" ):
        
        import os
        print os.getcwd()

        if type(codes_list) not in [tuple, list]:
            codes_list = [codes_list]
        
        self.counter = randint(0,1000000)
        
        self.current_name = self.mod_name+str(self.counter)
    
        file_list = []    
        
        self.codes_list = codes_list
    
        fh = []
        for i in range(len(codes_list)):
            fh.append( tempfile.NamedTemporaryFile(mode='w',suffix='.cpp') )

        for fh_,co in zip(fh,codes_list):
            fh_.write(co)
            fh_.seek(0)
        
            file_list.append( fh_.name )
        
        os.environ["CC"]="g++"
    
        setup_script = \
        """from distutils.core import setup, Extension\nmodule = Extension('{mod_name}', 
        sources = {file_list}, include_dirs = {include_dirs}, libraries = ['m'], 
        extra_compile_args = ['-I.','-std=c++11','-Ofast','-flto','-march=native','-funroll-loops'] )\nsetup(name = '{mod_name}',version = '1.0', ext_modules = [module])""".format(file_list=file_list,mod_name=self.current_name,include_dirs = include_dirs)
    
        fh2 = tempfile.NamedTemporaryFile(mode='w',suffix='.py')
        fh2.write(setup_script)
        fh2.seek(0)
    
        from distutils.core import run_setup
    
        dist = run_setup(fh2.name)
        dist.run_command("build")
    
        self.libname = "./build/lib.linux-x86_64-2.7/{mod_name}.so".format(mod_name=self.current_name)    
    
        if clean:
            dist.run_command("clean")
    
        self.builded_once = True
    
        import ctypes
        self.lib = ctypes.cdll.LoadLibrary(self.libname)
               
        
    def run(self, symbol,args):
        
        func = getattr(self.lib,symbol)
        func()
        
    def get_function(self, symbol):
        
        return getattr(self.lib,symbol)
        
    def __exit__(self):
        self.remove()
        
    def __del__(self):
        self.remove()
    
    def remove(self):
        import os
        if self.builded_once and os.path.isfile(self.libname):
            os.remove(self.libname)

def eqparser(formula, parameters=[], coefficients = [], inputs=[]):
    
    import re
    
    def generate_eq(dynvars, formula,var = "dXdt", ix='i'):

        eq = {}        
        
        for i,k in enumerate(formula.keys()):
            aux = formula[k]

            for j,k2 in enumerate(dynvars):
                aux = re.sub(r'\b'+ k2 + r'\b', "X[i+"+`j`+ "]", aux)  
    
            aux = re.sub(r'\bp\b', "p[j]", aux)
            aux = re.sub(r'\bg\b', "g[j]", aux)
                
            eq[k] = var+"["+ix+"+"+`i`+"]=" + aux + ";\n"
        
        return eq
    
    def replaces(eq,parameters,coefficients, inputs):
        
        for i,p in enumerate(parameters):
            eq = re.sub('\\b'+ p + '\\b', "pa[j+"+`i`+"*N]", eq)
    
        for i,p in enumerate(coefficients):
            eq = re.sub('\\b'+ p + '\\b', "co["+`i`+"]", eq)
    
        for i,p in enumerate(inputs):
            eq = re.sub('\\b'+ p + '\\b', "in["+`i`+"]", eq)
            
        return eq
    
    assert type(formula)==dict,"formula must be a dict"
    assert isinstance(parameters,(list,tuple)),"parameters must be a list"
    assert isinstance(inputs,(list,tuple)),"coefficients must be a list"
    assert 'g' in formula.keys(), "Variable g is needed"

    formula_ = formula.copy()
    formula_.pop('g')
    dynvars = formula_.keys()  
   
    main_eq = generate_eq(dynvars, formula_)
    main_eq = replaces( "".join(main_eq.values()), parameters,coefficients, inputs)

    g_assing = generate_eq(formula.keys(), {'g':formula['g']}, var = 'g', ix = 'j')
    g_assing = replaces(g_assing['g'],parameters,coefficients, inputs)
    
    n_inputs = len(inputs)
    n_eq = len(dynvars)
    n_parameters = len(parameters)
    n_coefficients = len(coefficients)

    return dynvars, g_assing, main_eq, n_eq, n_inputs, n_parameters, n_coefficients


def param_grid(**kwargs):
    import numpy as np

    assert len(kwargs)>0

    fixed = []
    explore = []

    for k,a in kwargs.iteritems():
        assert isinstance(a,(list,int,float,np.ndarray))
        if np.array(a).size == 1:
            fixed.append(k)
        else:
            explore.append(k)

    if len(explore)==1:
        
        flats = []
        flats.append(np.array(kwargs[explore[0]]).flatten())

        M = flats[0].size

        d_fixed = {k:kwargs[k]*np.ones(M) for k in fixed}
        d_explore = {k:flats[i] for i,k in enumerate(explore)}
        d_params = d_fixed.copy()
        d_params.update(d_explore)

        return d_params
    
    
    elif len(explore)>1:
        togrid = [kwargs[k] for k in explore]
        grids = np.meshgrid(*togrid)
        flats = []
        for g in grids:
            flats.append(g.flatten())

        M = flats[0].size

        d_fixed = {k:kwargs[k]*np.ones(M) for k in fixed}
        d_explore = {k:flats[i] for i,k in enumerate(explore)}
        d_params = d_fixed.copy()
        d_params.update(d_explore)

        return d_params

    else:
        return {k:kwargs[k] for k in fixed}

def funcs2code(fnspecs,gpu=False):

    """
    example:

    fnspecs = {'phi': (['x','a','b'], '-a*x*x*x+b*x*x' ) }

    __device__ float phi( float x,float a, float b);

    __device__ float phi( float x,float a, float b)
    {
        return -a*x*x*x+b*x*x;
    }
    """
    
    if gpu == True:
        s1 = "__device__ float "
    else:
        s1 = "float "
        
    s2 = ")\n{\n"
    s3 = "return "

    string = ""

    for fkey,fspec in fnspecs.iteritems():

        args = ",".join(['float '+aux for aux in  fspec[0] ])

        func = fspec[1]

        string+= s1 + fkey + "(" + args + ");\n"

    string+="\n\n"

    for fkey,fspec in fnspecs.iteritems():

        args = ",".join(['float '+aux for aux in  fspec[0] ])

        func = fspec[1]

        string+= s1 + fkey + "(" + args + s2 + s3 + func + ";\n}\n "

    return string


# import re 

# s = "ww*x[-2] + d*y + d0*x*x*y"

# print re.sub(r'x\[(.*)\]', r'linear_interpolation( X.data(), i + \1/step*n_vars )',s)
# #print re.sub(r'x\[(.*)\]', "a",s)

# s = "ww*x + d*y + d0*x*x*y"

# print re.sub(r'\bx\b', "a",s)