from setuptools import setup

version = '1.0'
long_description = 'Runs CWL tasks and workflows locally'

setup(
  name='cwlrunner',
  version=version,
  description=long_description,
  author='Scott Frazer',
  author_email='scott.d.frazer@gmail.com',
  packages=['cwlrunner'],
  install_requires=[
      "xtermcolor",
      "nose"
  ],
  scripts={
      'scripts/cwlrunner',
  },
  license = 'MIT',
  keywords = "Workflow, Task",
  url = "http://github.com/broadinstitute/common-workflow-language",
  classifiers=[
      'License :: OSI Approved :: MIT License',
      "Programming Language :: Python",
      "Development Status :: 4 - Beta",
      "Intended Audience :: Developers",
      "Natural Language :: English",
      "Topic :: Software Development :: Compilers"
  ]
)
