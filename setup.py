from distutils.core import setup

def readme():
    with open('README.md') as f:
        return f.read()

NAME = 'SASDocumentation'
VERSION = '0.1dev'
DESCRIPTION = 'A tool for analysising and documenting SAS code.'
LONG_DESCRIPTION = readme()
AUTHOR='Ben Corcoran'

PACKAGES=['SASDocumentation']
INSTALL_REQUIRES=['sphinx', 'recommonmark', 'sphinx-markdown-tables', 'matplotlib', 'numpy', 'networkx', 'm2r']


setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      author=AUTHOR,
      packages=PACKAGES,
      install_requires=INSTALL_REQUIRES,
      include_package_data=True,
      zip_safe=False)