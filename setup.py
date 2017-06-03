from setuptools import setup

setup(name='lingcorpora',
      version='0.2',
      description='API for National Corpus of Russian Language',
      url='https://github.com/alexeykosh/lingcorpora.py',
      author='Alexey Koshevoy',
      license='MIT',
      author_email='alexeykochevoy@gmail.com',
      packages=['lingcorpora'],
      zip_safe=False,
      install_requires=['bs4', 'requests', 'pandas'])
