from setuptools import setup, find_packages

requires = ['redis', ]
setup(name='eris',
      version='0.1.0',
      description='So what if you could import python code from redis...',
      long_description='I\'m not sure why you are using this, but good luck',
      author='Ross Delinger',
      author_email='rossdylan@csh.rit.edu',
      license='MIT',
      packages=find_packages(),
      install_requires=requires,
      zip_safe=False)
