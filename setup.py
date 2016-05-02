from distutils.core import setup, Extension
 
from sys import platform as _platform
if _platform == "linux" or _platform == "linux2":
    # module1 = Extension('jitcochlea/jitcochlea', sources = ['src/jitcochlea.cpp','src/cochlea.cpp'],include_dirs = ['src/'], extra_compile_args=['-Ofast','-flto','-march=native','-funroll-loops'] )
    setup (name = 'jitcochlea',
        version = '1.0',
        description = 'This is a demo package',
        # ext_modules = [module1],
        packages = ['jitcochlea'])

elif _platform == "darwin":
    # module1 = Extension('jitcochlea/jitcochlea', sources = ['src/jitcochlea.cpp','src/cochlea.cpp'],include_dirs = ['src/'], extra_compile_args=['-Ofast','-flto','-march=native','-funroll-loops'] )
    setup (name = 'jitcochlea',
        version = '1.0',
        description = 'This is a demo package',
        # ext_modules = [module1],
        packages = ['jitcochlea'])
    
elif _platform == "win32":

	pass

    # import sys
    # for a in sys.path:
    #     f = a.find('Anaconda')
    #     if f!=-1:
    #         path = a[:f+9]

    # import os
    
    # os.system("gcc.bat -mdll -O -Wall -Isrc/ -I"+path+"include -I"+path+"PC -c src/jitcochlea.cpp -o jitcochlea.o -Ofast -flto -march=native -funroll-loops") 
    # os.system("gcc.bat -mdll -O -Wall -Isrc/ -I"+path+"include -I"+path+"PC -c src/cochlea.cpp -o cochlea.o -Ofast -flto -march=native -funroll-loops") 
    # os.system("g++.bat -shared -s jitcochlea.o cochlea.o -o jitcochlea.dll") 
    
    # setup (name = 'jitcochlea',
    #         version = '1.0',
    #         description = 'This is a demo package',
    #         package_data={'jitcochlea': ['jitcochlea.dll']},
    #         packages = ['jitcochlea'])
