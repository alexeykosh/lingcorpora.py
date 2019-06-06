from setuptools import setup
from lingcorpora import __version__

setup(
    name='lingcorpora',
    version=__version__,
    description='API for text corpora',
    url='https://github.com/lingcorpora/lingcorpora.py',
    author='Ekaterina Gerasimenko, Artem Kopetsky, Alexey Koshevoy,' \
        'Mark Sobolev, Anna Zueva, Diana Malyshok, Maria Terekhina,' \
        'Ustinya Kosheleva and George Moroz',
    author_email='katgerasimenko@gmail.com',
    license='MIT',
    packages=['lingcorpora', 'lingcorpora.corpora'],
    python_requires='>=3.5',
    zip_safe=False,
    keywords = ['corpora', 'api', 'language'],
    install_requires=['bs4', 'requests', 'lxml', 'tqdm']
)
