from setuptools import setup
setup(
    name='sonosplay',
    version='0.1.0',
    packages=['sonosplay'],
    install_requires=['soco>=0.18.1'],
    entry_points={
        'console_scripts': [
            'sonosplay = sonosplay.main:main'
        ]
    })
