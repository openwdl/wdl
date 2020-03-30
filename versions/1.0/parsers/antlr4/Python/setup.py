from setuptools import setup, find_packages

setup(name='wdl_parser',
      version='1.0',
      description='Rudimentary WDL parser for processing WDL files',
      author='Patrick Magee',
      license='BSD 3-Clause "New" or "Revised" License',
      author_email='patrickmageee@gmail.com',
      url='https://github/openwdl/wdl',
      packages=find_packages(),
      install_requires=[
          "antlr4-python3-runtime==4.8",
          "pytest==5.3.5"
      ]
      )
