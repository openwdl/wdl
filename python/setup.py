from setuptools import setup

version = '1.0.5'
long_description = 'Runs WDL tasks and workflows locally'

setup(
  name='wdl',
  version=version,
  description=long_description,
  author='Scott Frazer',
  author_email='sfrazer@broadinstitute.org',
  packages=['wdl'],
  install_requires=[
      "xtermcolor",
      "nose"
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
