import json
import pickle

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
        )) if headers else None
        self.query_strings = query_strings
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
    def body_text(self):
        if self.body is None:
            return ''

        parsed_text = self.body.split('\r\n\r\n')
        return '\r\n\r\n'.join(parsed_text[1:]) \
            if len(parsed_text) > 1 else ''

    def __repr__(self):
        return self.body_text

    def to_dict(self):
        return {
            'path': self.path,
            'method': self.method,
            'headers': self.headers if self.headers else None,
            'query_strings': self.query_strings if self.query_strings else None,
            'form_params': self.form_params if self.form_params else None,
            'body_format': self.body_format.name if self.body_format else None,
            'body_text': self.body_text
        }


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


class ResourceExample:
    def __init__(self, request: ExampleRequest, response: ExampleResponse):
        self.request = request
        self.response = response

    def to_dict(self):
        return {
            'request': self.request.to_dict(),
            'response': self.response.to_dict()
        }

    def dump(self, pickle_filename):
        with open(pickle_filename, 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

    @classmethod
    def load(cls, pickle_filename) -> 'ResourceExample':
        with open(pickle_filename, 'rb') as f:
            return pickle.load(f)
