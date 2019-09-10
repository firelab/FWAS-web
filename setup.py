#!/usr/bin/env python

from setuptools import setup, find_packages


def read_requirements(filename):
    with open(filename) as f:
        requirements = [
            line[:line.find('#')] for line in f.read().splitlines()
            if not line.startswith('-i') and not line.startswith('#')
        ]


with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = read_requirements('requirements.txt')
test_requirements = read_requirements('dev-requirements.txt')

setup(
    author="Levi Malott",
    author_email='levi@third.consulting',
    classifiers=[
        'Intended Audience :: Developers',

        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
    ],
    description="Register alert criteria and receive notifications on weather.",
    entry_points={
        'console_scripts': [
            'fwas=fwas.cli:cli',
        ],
    },
    install_requires=requirements,
    long_description=readme,
    include_package_data=True,
    keywords='fwas',
    name='fwas',
    packages=find_packages(include=['fwas']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/ldmalott/fwas',
    version='0.1.0',
    zip_safe=False,
)

