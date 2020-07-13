from setuptools import setup, Extension ,find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
	
setup(
    name="mftool",
    version="1.1",
    author="Avanish Pandey",
    author_email="ap@astaqc.com",
    description="Python library for extracting realtime Mutual funds data from AMFI (India)",
    license="MIT",
    keywords="amfi, quote, mutual-funds, funds, bse, nse, market, stock, stocks",
    install_requires=['requests','bs4','sqlalchemy'],
    url="https://github.com/astaqc/mftool",
    packages=find_packages(),
	long_description = long_description,
	long_description_content_type='text/markdown'
)
