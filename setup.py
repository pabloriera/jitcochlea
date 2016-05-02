from setuptools	 import setup, Extension
from sys import platform as _platform

# from setuptools.command.install_scripts import install_scripts
# from setuptools.command.install import install
# from distutils import log # needed for outputting information messages 


# class OverrideInstall(install):

#     def run(self):
#     	print "OVERRIDED"
#         uid, gid = 0, 0
#         mode = 0700
#         install.run(self) # calling install.run(self) insures that everything that happened previously still happens, so the installation does not break! 
#         # here we start with doing our overriding and private magic ..
#         print "O:", self.get_outputs()
#         print "O2:", self.install_scripts
#         for filepath in self.get_outputs():
#             if self.install_scripts in filepath:
#             	print "A:",filepath
#                 # log.info("Overriding setuptools mode of scripts ...")
#                 # log.info("Changing ownership of %s to uid:%s gid %s" %
#                 #          (filepath, uid, gid))
#                 # os.chown(filepath, uid, gid)
#                 # log.info("Changing permissions of %s to %s" %
#                 #          (filepath, oct(mode)))
#                 # os.chmod(filepath, mode)


if _platform == "linux" or _platform == "linux2":
    setup (name = 'jitcochlea',
        version = '1.0',
        description = 'Cochlea dynamical model',
        packages = ['jitcochlea'],
        data_files=[('src',['src/cochlea.cpp','src/jitcochlea.cpp','src/cochlea.hpp']) ])
        # cmdclass={'install': OverrideInstall})

elif _platform == "darwin":
    setup (name = 'jitcochlea',
        version = '1.0',
        description = 'Cochlea dynamical model',
        packages = ['jitcochlea'])
    
elif _platform == "win32":

	pass

