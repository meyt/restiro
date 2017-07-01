import re
import os.path
from setuptools import setup


# reading package's version (same way sqlalchemy does)
with open(os.path.join(os.path.dirname(__file__), 'webtest_docgen', '__init__.py')) as v_file:
    package_version = re.compile(r".*__version__ = '(.*?)'", re.S).match(v_file.read()).group(1)

setup(
    name='webtest_docgen',
    version=package_version,
    description='Generate RESTful API documentation from webtest tests',
    long_description=open('README.rst').read(),
    url='http://github.com/meyt/webtest-docgen',
    author='Mahdi Ghane.g',
    license='GPLv3',
    keywords='api_documentation api document_generator raml_client_builder',
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
    packages=['webtest_docgen'],
    install_requires=[
        'webtest >= 2.0.27'
    ],
    include_package_data=True,
    zip_safe=False
)
