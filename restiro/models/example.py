import json

from typing import Union

from restiro.helpers import CaseInsensitiveDict


class BodyFormat:
    name = None
    header_mime = None


class BodyFormatJson(BodyFormat):
    name = 'json'
    header_mime = 'application/json'


class BodyFormatText(BodyFormat):
    name = 'text'
    header_mime = 'text/plain'


class BodyFormatXml(BodyFormat):
    name = 'xml'
    header_mime = 'application/xml'


class BodyFormatYaml(BodyFormat):
    name = 'yaml'
    header_mime = 'application/x-yaml'


class ExampleRequest:
    def __init__(self, path: str, method: str, headers: dict = None,
                 query_strings: dict = None, form_params: dict = None,
                 body: str = None):
        self.path = path
        self.method = method
        self.headers = dict(map(
            lambda x: (x[0].lower(), x[1]),
            headers.items()
        )) if headers else dict()
        self.query_strings = query_strings or {}
        self.form_params = form_params
        self.body = body

    @property
    def body_format(self) -> Union[BodyFormat, None]:
        content_type_raw = CaseInsensitiveDict(self.headers).\
            get('Content-Type', None)
        return {
            BodyFormatJson.header_mime: BodyFormatJson,
            BodyFormatYaml.header_mime: BodyFormatYaml,
            BodyFormatXml.header_mime: BodyFormatXml
        }.get(content_type_raw.split(';', 1)[0], None) \
            if content_type_raw else None

    @property
    def formatted_body(self):
        # TODO Other formats not supported at yet
        if self.body_format == BodyFormatJson:
            return json.loads(self.body)

    def __repr__(self):
        sections = [
            '%s %s' % (self.method, self.path),
            self.repr_headers()
        ]
        if self.body:
            sections.append(self.body)
        return '\n\n'.join(sections)

    def repr_headers(self):
        return '\n'.join('%s: %s' % header for header in self.headers.items())

    def to_dict(self):
        return {
            'path': self.path,
            'method': self.method,
            'headers': self.headers if self.headers else None,
            'query_strings': self.query_strings if self.query_strings else None,
            'form_params': self.form_params if self.form_params else None,
            'body_format': self.body_format.name if self.body_format else None,
            'body': self.body
        }

    @classmethod
    def create_from_dict(cls, data: dict) -> 'ExampleRequest':
        return cls(
            path=data['path'],
            method=data['method'],
            headers=data['headers'],
            query_strings=data['query_strings'],
            form_params=data['form_params'],
            body=data['body']
        )


class ExampleResponse:

    def __init__(self, status: int, headers: dict, body: str, reason: str=None):
        self.status = status
        self.headers = dict(map(
            lambda x: (x[0].lower(), x[1]),
            headers.items()
        ))
        self.body = body
        self.reason = reason

    @property
    def body_format(self) -> Union[BodyFormat, None]:
        content_type_raw = CaseInsensitiveDict(self.headers).\
            get('Content-Type', None)
        return {
            BodyFormatJson.header_mime: BodyFormatJson,
            BodyFormatYaml.header_mime: BodyFormatYaml,
            BodyFormatXml.header_mime: BodyFormatXml
        }.get(content_type_raw.split(';', 1)[0], None) \
            if content_type_raw else None

    @property
    def body_json(self):
        return json.dumps(self.body, indent=4)

    def to_dict(self):
        return {
            'status': self.status,
            'reason': self.reason,
            'headers': self.headers,
            'body_format': self.body_format.name if self.body_format else None,
            'body': self.body
        }

    def repr_headers(self):
        return '\n'.join('%s: %s' % header for header in self.headers.items())

    def __repr__(self):
        return '%s%s' % (
            self.repr_headers(),
            '\r\n\r\n%s' % self.body
        )

    @classmethod
    def create_from_dict(cls, data: dict) -> 'ExampleResponse':
        return cls(
            status=data['status'],
            headers=data['headers'],
            body=data['body'],
            reason=data['reason']
        )


class ResourceExample:
    def __init__(self, request: ExampleRequest, response: ExampleResponse,
                 visible: bool=False):
        self.request = request
        self.response = response
        self.visible = visible

    def to_dict(self):
        return {
            'request': self.request.to_dict(),
            'response': self.response.to_dict(),
            'visible': self.visible
        }

    def dump(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f)

    @classmethod
    def load(cls, filename) -> 'ResourceExample':
        with open(filename, 'r') as f:
            return cls.create_from_dict(json.load(f))

    @classmethod
    def create_from_dict(cls, data: dict) -> 'ResourceExample':
        return cls(
            request=ExampleRequest.create_from_dict(data['request']),
            response=ExampleResponse.create_from_dict(data['response']),
            visible=data['visible']
        )
