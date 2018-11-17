"""Setup module for PyPI / pip integration.
"""

import setuptools


with open('readme.md', encoding='utf-8') as file:
    LONG_DESCRIPTION = file.read()
    # long_description = long_description.split('<!---START--->')[-1]
    #                                    .split('<!---END--->')[0]
    # long_description = long_description.replace('<!---PYPI', '')
    # long_description = long_description.replace('PYPI--->', '')

setuptools.setup(
    name='cutie',
    version='0.2.2',
    author='Hans / Kamik423',
    author_email='contact.kamik423@gmail.com',
    description='Commandline User Tools for Input Easification',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/kamik423/cutie',
    py_modules=['cutie'],
    license='MIT',
    install_requires=['colorama', 'readchar'],
    python_requires='>=3.5',
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
