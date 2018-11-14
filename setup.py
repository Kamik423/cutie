import setuptools

with open('readme.md', encoding='utf-8') as file:
    long_description = file.read().split('<!---START--->')[-1].split('<!---END--->')[0]
    long_description = long_description.replace('<!---PYPI', '')
    long_description = long_description.replace('PYPI--->', '')

setuptools.setup(
    name='cutie',
    version='0.0.5',
    author='Hans',
    author_email='contact.kamik423@gmail.com',
    description='Commandline User Tools for Input Easification',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/kamik423/cutie',
    packages=setuptools.find_packages(),
    license='MIT',
    install_requires=['colorama', 'readchar'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)