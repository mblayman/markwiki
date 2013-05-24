# Copyright (c) 2013, Matt Layman
'''
MarkWiki
========

MarkWiki is a simple wiki using Markdown.

Follow development on `GitHub <https://github.com/mblayman/markwiki>`_.
'''

from setuptools import setup, find_packages

setup(
    name='MarkWiki',
    version='1.0',
    url='https://github.com/mblayman/markwiki',
    license='BSD',
    author='Matt Layman',
    author_email='matthewlayman@gmail.com',
    description='A simple wiki using Markdown',
    long_description=__doc__,
    packages=['markwiki'],
    entry_points={
        'console_scripts': ['markwiki = markwiki.server:run']
    },
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask',
        'Markdown',
        'Pygments',
    ]
)
