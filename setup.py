# Copyright (c) 2016, Matt Layman
'''
Follow MarkWiki development on `GitHub
<https://github.com/mblayman/markwiki>`_. Developer documentation is on
`Read the Docs <https://markwiki.readthedocs.org/>`_.
'''

from setuptools import find_packages, setup
import sys

__version__ = '1.6'

# The docs import setup.py for the version so only call setup when not behaving
# as a module.
if __name__ == '__main__':
    with open('docs/releases.rst', 'r') as f:
        releases = f.read()

    long_description = __doc__ + '\n\n' + releases

    install_requires = [
        'argparse==1.2.1',
        'Flask==0.10.1',
        'Flask-Login==0.2.9',
        'Flask-WTF==0.9.4',
        'Frozen-Flask==0.11',
        'Markdown==2.3.1',
        'Pygments==1.6',
        'requests==2.6.0',
        'Whoosh==2.5.6',
        'sh==1.11',
    ]

    # Add some developer tools.
    if 'develop' in sys.argv:
        install_requires.extend([
            'coverage==3.7.1',
            'gunicorn==18.0',
            'nose==1.3.0',
            'pep8',
        ])

    setup(
        name='MarkWiki',
        version=__version__,
        url='https://github.com/mblayman/markwiki',
        license='BSD',
        author='Matt Layman',
        author_email='matthewlayman@gmail.com',
        description='A simple wiki using Markdown',
        long_description=long_description,
        packages=find_packages(),
        entry_points={
            'console_scripts': ['markwiki = markwiki.server:run']
        },
        include_package_data=True,
        zip_safe=False,
        install_requires=install_requires,
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Web Environment',
            'Framework :: Flask',
            'License :: OSI Approved :: BSD License',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Topic :: Internet',
        ],
        test_suite='markwiki.tests'
    )
