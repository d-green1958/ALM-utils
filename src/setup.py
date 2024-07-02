from setuptools import setup, find_packages

version = "1.0.0"

def get_version():
    return version

setup(
    name='ALM-utils',
    version=get_version(),
    packages=find_packages(),
    install_requires=[
        # Add any dependencies your package needs here
    ],
    # Metadata
    author='Dylan Green',
    description='Utilities for openFoam v2006 Actuator Line Model '
)
