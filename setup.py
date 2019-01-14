from setuptools import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import numpy
import sys

setup(
    name = 'watershed',
    version = '0.1.2',
    packages = ['watershed'],
    ext_modules = cythonize([Extension('watershed._watershed', ['watershed/_watershed.pyx'], include_dirs = [numpy.get_include()])], compiler_directives={'language_level':sys.version_info[0]}),
    setup_requires = [
        'cython',
        'numpy'
    ],
    install_requires = [
        'numpy',
        'rasterio',
        'fiona'
    ],
    include_dirs = [numpy.get_include()],
    license = "MIT"
)
