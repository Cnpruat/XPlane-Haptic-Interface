from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext

ext_modules = [
    Pybind11Extension(
        "tactcombine",                        # Nom du module côté Python
        ["tactcombine.cpp"],                     # Fichier C++ à compiler
        include_dirs=["."],                  # Pour nlohmann si tu mets le .hpp localement
    ),
]

setup(
    name="tactcombine",
    version="0.1",
    description="Combinateur de .tact en C++",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
)
