from setuptools import setup

version = '1.0.8'
long_description = 'Parse and Process WDL Files'

setup(
  name='wdl',
  version=version,
  description=long_description,
  author='Scott Frazer',
  author_email='sfrazer@broadinstitute.org',
  packages=['wdl'],
  install_requires=[
      "xtermcolor",
      "pytest"
  ],
  scripts={
      'scripts/wdl',
  },
  license = 'MIT',
  keywords = "Workflow, Task",
  url = "http://github.com/broadinstitute/wdl",
  classifiers=[
      'License :: OSI Approved :: MIT License',
      "Programming Language :: Python",
      "Development Status :: 4 - Beta",
      "Intended Audience :: Developers",
      "Natural Language :: English"
  ]
)
