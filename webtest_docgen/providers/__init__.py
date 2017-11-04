"""Documentation Providers
To creating final output of documentation from defined models and 
tests result, we need providers.
official providers should not use third-party libraries, but for having
a "featureful" one, we can inherit the ``BaseProvider`` and implement it.
"""
from .base import BaseProvider
from .json import JSONProvider
from .markdown import MarkdownProvider
