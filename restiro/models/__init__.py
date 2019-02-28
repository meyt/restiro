"""
    API Documentation models, mostly based on RAML 0.8
"""
from .parameters import URLParam, QueryParam, HeaderParam, FormParam, Param
from .example import (
    ResourceExample,
    ExampleResponse,
    ExampleRequest,
    BodyFormat,
    BodyFormatJson,
    BodyFormatYaml,
    BodyFormatXml
)
from .resource import Resource, Resources
from .document import Document
from .root import DocumentationRoot
