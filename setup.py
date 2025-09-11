from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="simple_sis_api",
    version="0.1",
    description="Simple Client for SIS Web Services API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Prabha Acharya",
    author_email="pacharya@caltech.edu",
    python_requires=">=3.11",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent"
    ],
    packages=["simple_sis_api"],
    include_package_data=True,
    install_requires=["requests"]
)