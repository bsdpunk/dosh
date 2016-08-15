#from distutils.core import setup
from setuptools import setup, find_packages

#dependecy_links = ["git+https://github.com/pexpect/pexpect.git#egg=pexpect-0.1"]
#install_requires = ['pyvmomi','pyvim']

setup(
    name='dosh',
    version='0.01',
    packages=['dosh',],
    #install_requires=install_requires,
    entry_points = { 'console_scripts': [
        "dosh = dosh.dosh:cli", ],
        },
    author = "Dusty C",
    author_email = "bsdpunk@gmail.com.com",
    description = "Remote shell for docker",
    license = "BSD",
    keywords = "Shell cli terminal financial data",
    url = 'bsdpunk.blogspot.com'   
    )
