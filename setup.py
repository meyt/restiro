import re

from os.path import dirname, join
from setuptools import setup, find_packages


# Read package version
with open(join(dirname(__file__), 'restiro', '__init__.py')) as f:
    package_version = re.compile(r".*__version__ = '(.*?)'",
                                 re.S).match(f.read()).group(1)

setup(
    name='restiro',
    version=package_version,
    description='RESTful API documentation generator',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='http://github.com/meyt/restiro',
    author='Mahdi Ghane.g',
    license='GPLv3',
    keywords='api_documentation api document_generator',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Documentation',
        'Topic :: Documentation',
        'Topic :: Software Development :: Build Tools'
    ],
    packages=find_packages(),
    install_requires=[],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'restiro = restiro.cli:main',
            'restiro-mock = restiro.cli:mock'
        ]
    }
)
