from setuptools import setup

setup(
    name='bettadb',
    version='0.1.1',
    description='Simple-to-use embedded database, modelled on MongoDB',
    author='Jack Stephenson <jackatbancast>',
    author_email='jack@bancast.net',
    url='https://github.com/ideaxod/bettaDB.git',
    packages=['bettadb'],
    install_requires=['eventedpy']
)
