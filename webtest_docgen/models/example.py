import json
from typing import Union
from webtest_docgen.utils import CaseInsensitiveDict


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


class Request:
    def __init__(self, path: str, method: str, headers: dict=None,
                 query_strings: dict=None, form_params: dict=None):
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
            'headers': self.headers if self.headers else None,
            'query_strings': self.query_strings if self.query_strings else None,
            'form_params': self.form_params if self.form_params else None
        }


class Response:

    def __init__(self, status: int, headers: dict, body: bytes):
        self.status = status
        self.headers = headers
        self.body = body

    @property
    def body_format(self) -> Union[BodyFormat, None]:
        content_type_raw = CaseInsensitiveDict(self.headers).get('Content-Type', None)
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
            'headers': self.headers,
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
