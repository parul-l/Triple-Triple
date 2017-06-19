import sys

from setuptools import setup


python_version = sys.version_info[:2]
if python_version < (2, 7) or (3, 0) <= python_version < (3, 3):
    raise RuntimeError('Python version 2.7 or >= 3.3 required.')


classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: MIT License',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: POSIX :: Linux',
    'Operating System :: Unix',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Topic :: Scientific/Engineering :: Mathematics'
]

install_requires = ['numpy>=1.9']

keywords = [
    'simulation',
    'nba',
    'prediction',
]

packages = [
    'triple_triple',
    'triple_triple.data_generators',
]

tests_require = []

if python_version[0] == 2:
    tests_require.append('mock')

setup(
    author='Parul Laul',
    author_email='parul.laul@gmail.com',
    description='NBA game simulator',
    classifiers=classifiers,
    install_requires=install_requires,
    keywords=keywords,
    license='MIT',
    name='triple-triple',
    packages=packages,
    tests_require=tests_require,
    test_suite='nose.collector',
    url='https://github.com/parul-l/Triple-Triple',
    version='0.1'
)
