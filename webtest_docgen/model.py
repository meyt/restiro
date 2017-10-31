"""
    Resources model based on RAML 0.8
"""
import re
import json
from typing import Union


class Document:

    def __init__(self, title, content=None):
        self.title, self.content = title, content

    @property
    def __filename__(self):
        return re.sub("[\x00-\x2F\x3A-\x40\x5B-\x60\x7B-\x7F]+", "-", self.title).lower()

    def to_dict(self):
        return {
            'title': self.title,
            'content': self.content
        }


class BodyFormat:
    name = None
    header_mime = None


class BodyFormatJson(BodyFormat):
    name = 'json'
    header_mime = 'application/json'


class BodyFormatXml(BodyFormat):
    name = 'xml'
    header_mime = 'application/xml'


class BodyFormatYaml(BodyFormat):
    name = 'yaml'
    header_mime = 'application/x-yaml'


class Resource:

    def __init__(self, path: str, method: str, display_name: str=None,
                 description: str=None, params=None):
        self.path = path
        self.method = method
        self.display_name = display_name
        self.description = description
        self.uri_params = []
        self.query_params = []
        self.form_params = []
        self.header_params = []
        self.examples = []

        if params:
            if isinstance(params, (list, tuple)):
                self.set_params(*params)
            else:
                self.set_params(params)

    def set_params(self, *args):
        for item in args:
            if isinstance(item, UriParam):
                self.uri_params.append(item)

            elif isinstance(item, QueryParam):
                self.query_params.append(item)

            elif isinstance(item, FormParam):
                self.form_params.append(item)

            elif isinstance(item, HeaderParam):
                self.header_params.append(item)
        return self

    @property
    def __key__(self):
        return '%s-%s' % (self.path, self.method)

    @property
    def __filename__(self):
        return str(self.__key__).lstrip('/').replace('/', '-')

    def to_dict(self):
        return {
            'path': self.path,
            'method': self.method,
            'display_name': self.display_name,
            'description': self.description,
            'header_params': [param.to_dict() for param in self.header_params],
            'uri_params': [param.to_dict() for param in self.uri_params],
            'query_params': [param.to_dict() for param in self.query_params],
            'form_params': [param.to_dict() for param in self.form_params],
            'examples': [example.to_dict() for example in self.examples]
        }

    def __repr__(self):
        return '%s %s' % (self.method.upper(), self.path)


class Resources(dict):

    def append(self, resource: Resource):
        if not isinstance(resource, Resource):
            raise TypeError('item is not of type Resource')
        self[resource.__key__] = resource

    def find(self, path, method) -> Resource:
        return self.get('%s-%s' % (path, method), None)

    @property
    def __tree__(self):
        """
        Get tree of resources
        First level: resource
        Second level: method
        :return: 
        """
        result = {}
        for resource_key, resource in self.items():
            result.setdefault(resource.path, {})
            result[resource.path].setdefault(resource.method, [])
            result[resource.path][resource.method].append(resource)
        return result

    def to_dict(self):
        return [resource.to_dict() for resource_key, resource in self.items()]


class Request:
    def __init__(self, path, method, headers=None,
                 query_strings=None, form_params=None):
        self.path = path
        self.method = method
        self.headers = headers
        self.query_strings = query_strings
        self.form_params = form_params

    def __repr__(self):
        result = '%s %s' % (self.method.upper(), self.path)
        if self.headers:
            result += '\n%s' % '\n'.join('%s: %s' % header for header in self.headers.items())

        if self.form_params:
            result += '\n\n%s' % '\n'.join('%s: %s' % param for param in self.form_params.items())

        return result

    def to_dict(self):
        return {
            'path': self.path,
            'method': self.method,
            'headers': dict(self.headers) if self.headers else None,
            'query_strings': dict(self.query_strings) if self.query_strings else None,
            'form_params': self.form_params if self.form_params else None
        }


class Response:

    def __init__(self, status: int, headers: dict, body: bytes):
        self.status = status
        self.headers = headers
        self.body = body

    @property
    def body_format(self) -> Union[BodyFormat, None]:
        content_type_raw = self.headers.get('Content-type', None)
        return {
            BodyFormatJson.header_mime: BodyFormatJson,
            BodyFormatYaml.header_mime: BodyFormatYaml,
            BodyFormatXml.header_mime: BodyFormatXml
        }.get(content_type_raw.split(';', 1)[0], None) if content_type_raw else None

    @property
    def body_json(self):
        return json.loads(self.body)

    def to_dict(self):
        return {
            'status': self.status,
            'headers': dict(self.headers),
            'body': self.body.decode(),
            'body_format': self.body_format.name if self.body_format else None
        }

    def __repr__(self):
        return '%s%s' % (
            '%s' % '\n'.join('%s: %s' % header for header in self.headers.items()),
            '\n\n%s' % self.body
        )


class ResourceExample:
    def __init__(self, request: Request, response: Response):
        self.request = request
        self.response = response

    def to_dict(self):
        return {
            'request': self.request.to_dict(),
            'response': self.response.to_dict()
        }


class Param:
    def __init__(self, name=None, display_name=None, description=None, type_=None, enum=None,
                 pattern=None, min_length=None, max_length=None, minimum=None, maximum=None,
                 example=None, repeat=None, required=None, default=None, media_type=None):
        self.name = name
        self.display_name = display_name
        self.description = description
        self.type_ = type_
        self.enum = enum
        self.pattern = pattern
        self.min_length = min_length
        self.max_length = max_length
        self.minimum = minimum
        self.maximum = maximum
        self.example = example
        self.repeat = repeat
        self.required = required
        self.default = default
        self.media_type = media_type

    def to_dict(self):
        return {
            'name': self.name,
            'display_name': self.display_name,
            'description': self.description,
            'type': self.type_,
            'enum': self.enum,
            'pattern': self.pattern,
            'min_length': self.min_length,
            'max_length': self.max_length,
            'minimum': self.minimum,
            'maximum': self.maximum,
            'example': self.example,
            'repeat': self.repeat,
            'required': self.required,
            'default': self.default,
            'media_type': self.media_type
        }


class UriParam(Param):
    pass


class QueryParam(Param):
    pass


class FormParam(Param):
    pass


class HeaderParam(Param):
    pass


class Documents(list):

    def append(self, document: Document):
        if not isinstance(document, Document):
            raise TypeError('item is not of type Document')
        super().append(document)

    def to_dict(self):
        return [document.to_dict() for document in self]


class DocumentationRoot:

    def __init__(self, title=None, version='1', media_type=None,
                 base_uri=None, base_uri_params=None,
                 protocols=None, resources=None, documents=None):
        self.title = title
        self.version = version
        self.media_type = media_type
        self.base_uri = base_uri
        self.base_uri_params = [] or base_uri_params
        self.protocols = [] or protocols
        self.documents = Documents()
        self.resources = Resources()

        if documents:
            if isinstance(documents, (tuple, list)):
                self.set_documents(*documents)
            else:
                self.set_documents(documents)

        if resources:
            if isinstance(resources, (tuple, list)):
                self.set_resources(*resources)
            else:
                self.set_resources(resources)

    def set_resources(self, *args):
        for item in args:
            self.resources.append(item)
        return self

    def set_documents(self, *args):
        for item in args:
            self.documents.append(item)
        return self

    def to_dict(self):
        return {
            'title': self.title,
            'version': self.version,
            'base_uri': self.base_uri,
            'media_type': self.media_type,
            'protocols': self.protocols,
            'documents': self.documents.to_dict(),
            'resource': self.resources.to_dict(),
            'base_uri_params': self.base_uri
        }
