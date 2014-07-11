from distutils.core import setup
from Cython.Build import cythonize
import numpy

setup(
    name = 'watershed',
    version = '0.1',
    packages = find_packages(),
    ext_modules = cythonize('_watershed.pyx'),
    include_dirs = [numpy.get_include()],
    license = "MIT"
)
