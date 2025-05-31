# setup.py
from setuptools import setup, Extension
from pybind11.setup_helpers import build_ext, Pybind11Extension
import sysconfig

ext_modules = [
    Pybind11Extension(
        "xiangqi_cpp",
        ["cpp_implement/bindings.cpp", "cpp_implement/engine.cpp"],  # include bindings.cpp
        include_dirs=[
            sysconfig.get_paths()["include"],  # Python headers
        ],
        library_dirs=[
            sysconfig.get_config_var("LIBDIR") or "C:/Users/Manh Duc/AppData/Local/Programs/Python/Python310/libs"
        ],
        language="c++"
    ),
]
setup(
    name="xiangqi_cpp",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
)
