import os
from setuptools import setup


setup(
    name='TARAVisualize',
    version='0.1.0',
    description='',
    url='',
    author='Christopher Neely',
    author_email='christopher.neely1200@gmail.com',
    license='GNU GPL 3',
    packages=["TARAVisualize", "TARAVisualize.components", "TARAVisualize.loader", "TARAVisualize.utils"],
    python_requires='>=3.7',
    install_requires=open(os.path.join(os.path.dirname(__file__), "_requirements.txt")).readlines(),
)
