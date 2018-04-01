from setuptools import setup

setup(name='lingcorpora',
      version='1.0',
      description='API for corpora',
      url='https://github.com/lingcorpora/lingcorpora.py',
      author='Alexey Koshevoy, Artem Kopetsky, Ekaterina Gerasimenko, Maria Terekhina',
      license='MIT',
      author_email='alexeykochevoy@gmail.com',
      packages=['lingcorpora'],
      zip_safe=False,
      keywords = ['corpora', 'api', 'language']
      install_requires=['bs4', 'requests', 'lxml', 'tqdm'])
