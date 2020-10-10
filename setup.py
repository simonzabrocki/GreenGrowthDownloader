from setuptools import setup, find_packages

setup(
    name='ggdata',
    version='0.1.22',
    description='A Python package for downloading data from public APIs',
    url='https://github.com/simonzabrocki/GreenGrowthDownloader',
    author='Simon Zabrocki',
    author_email='simon.zabrocki@gmail.com',
    license='BSD 2-clause',
    install_requires=[],
    packages=find_packages(),
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6',
    ],
    include_package_data=True,
    package_data={
        '': ['params/*.json']
    }
)
