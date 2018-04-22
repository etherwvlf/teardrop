import os
from setuptools import setup, find_packages

setup(
    name = 'teardrop',
    version = '0.5.2',
    description = 'Teardrop',
    long_description = 'Teardrop - Memory Dwelling Webchat',
    url = '',
    license = 'Chlorine, Inc.',
    author = '',
    author_email = '',
    packages = [''],
    include_package_data = True,
    package_data = {'': ['templates/*.html']},
    install_requires = ["flask", "stem"],
    classifiers = [ 'Development Status :: 7 - Beta',
                    'Programming Language :: Python'],
    entry_points = { 'console_scripts':
                        [ 'teardrop = teardrop:main']}
)
