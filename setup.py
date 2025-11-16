from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np

# ------------------------------------------------------
# Define extension modules
# ------------------------------------------------------
extensions = [
    Extension(
        "pygbm.base",
        ["src/pygbm/base.pyx"],
        include_dirs=[np.get_include()],
    ),
    Extension(
        "pygbm.gbm_simulator",
        ["src/pygbm/gbm_simulator.pyx"],
        include_dirs=[np.get_include()],
    ),
    Extension(
        "pygbm.main",
        ["src/pygbm/main.pyx"],
        include_dirs=[np.get_include()],
    ),
]

# ------------------------------------------------------
# Setup configuration
# ------------------------------------------------------
setup(
    name="pygbm",
    version="0.1.0",

    package_dir={"": "src"},
    packages=["pygbm"],

    # Build the cython extensions
    ext_modules=cythonize(
        extensions,
        compiler_directives={
            "language_level": "3",
            "embedsignature": True,
        },
    ),

    # Ship only compiled extensions, exclude .py and .pyx
    package_data={"pygbm": ["*.so", "*.pyd"]},
    exclude_package_data={"pygbm": ["*.py", "*.pyx"]},

    zip_safe=False,
)

