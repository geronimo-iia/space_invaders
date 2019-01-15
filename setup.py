# -*- coding: utf-8 -*-
import re
# https://packaging.python.org/en/latest/distributing.html

from setuptools import setup, find_packages
import os


def get_version():
    from space_invaders import __version__
    return __version__


with open(os.path.join(os.path.dirname(__file__), 'LICENSE')) as f:
    _license = f.read()

setup(
    name='space_invaders',
    version=get_version(),
    description='Space Invaders',
    long_description='Space Invaders',
    author='Jerome Guibert',
    author_email='jguibert@gmail.com',
    url='https://github.com/geronimo-iia/space_invaders.git',
    license=_license,
    packages=find_packages(exclude=('tests', 'docs', 'bin')),
    package_dir={"space_invaders": "space_invaders", "engine": "engine"},
    package_data={
        'data': ['*.*'],
    },
    install_requires=[
        'pygame'
    ],
    include_package_data=True,
    zip_safe=False,
    platforms="any",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7'
    ],
    keywords='Pygame',

)
