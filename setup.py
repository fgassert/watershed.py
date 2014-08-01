from setuptools import setup 
from distutils.extension import Extension
from Cython.Build import cythonize
import numpy

setup(
    name = 'watershed',
    version = '0.1.1',
    packages = ['watershed'],
    ext_modules = cythonize([Extension('watershed._watershed', ['watershed/_watershed.pyx'])]),
    setup_requires = [
        'cython>=0.20',
        'numpy'
    ],
    install_requires = [
        'numpy',
        'gdal==1.9.0',
        'rasterio>=0.9',
        'fiona'
    ],

    include_dirs = [numpy.get_include()],
    license = "MIT"
)
