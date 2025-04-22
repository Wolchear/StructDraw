from setuptools import setup, find_packages

setup(
    name="struct_draw",
    version="0.1.0",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "numpy>=1.26.1,<2.0",
        "Pillow>=11.1.0,<12.0"
    ],
    author="",
    author_email="",
    description="A Python package for plotting protein secondary structure from DSSP/Stride outputs",
    url="https://github.com/Wolchear/StructDraw",
    license="BSD-3-Clause",
)
