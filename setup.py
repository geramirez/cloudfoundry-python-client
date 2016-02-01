''' Setup script for CloudFoundry package module '''

from setuptools import setup

dependencies = ['requests']

setup(
    name='CloudFoundry',
    version='0.1',
    packages=['cloudfoundry'],
    description='Liteweight client for CloudFoundry',
    author='Gabriel Ramirez',
    install_requires=dependencies,
    keywords=['client', 'Cloud Foundry', 'Cloud.gov'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Operating System :: Unix',
        'Operating System :: MacOS'
    ]
)
