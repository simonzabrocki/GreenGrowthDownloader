from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()
    required = [r.split('==')[0] for r in required]

setup(
    name='ggdata',
    version='0.1.32',
    description='A Python package for downloading data from public APIs',
    url='https://github.com/simonzabrocki/GreenGrowthDownloader',
    author='Simon Zabrocki',
    author_email='simon.zabrocki@gmail.com',
    license='BSD 2-clause',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=required,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6',
    ],
    scripts=['ggdownload'],
    package_data={
        '': ['params/*.json', 'params/*.csv']
    },
)
