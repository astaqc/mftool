from setuptools import setup, Extension ,find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
	
setup(
    name="mftool",
<<<<<<< HEAD
    version="1.6",
    author="Sujit Nayakwadi",
    author_email="nayakwadi.sujit@gmail.com",
    description="Library for extracting real time Mutual funds data in India",
=======
    version="1.1",
    author="Avanish Pandey",
    author_email="ap@astaqc.com",
    description="Python library for extracting realtime Mutual funds data from AMFI (India)",
>>>>>>> 6b40e10690dafa427a0773728cfd4bdee7013004
    license="MIT",
    keywords="amfi, quote, mutual-funds, funds, bse, nse, market, stock, stocks",
    install_requires=['requests','bs4','sqlalchemy'],
    url="https://github.com/astaqc/mftool",
    packages=find_packages(),
	long_description = long_description,
	long_description_content_type='text/markdown',
	package_data = {'': ['*.json']}
)
