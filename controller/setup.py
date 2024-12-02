from setuptools import setup

setup(
    name='ictester',
    version='1.0',    
    description='IC tester controller',
    url='https://github.com/jakubfi/ictester',
    author='Jakub Filipowicz',
    author_email='jakubf@mera400.pl',    
    license='MIT',
    packages=['ictester', 'ictester/parts'],
    install_requires=['pyserial', 'colorama'],

    entry_points={
        'console_scripts': ['ictester = ictester.ictester:main'],
    },
)
