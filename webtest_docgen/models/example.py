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
    def __init__(self, path: str, method: str, headers: dict = None,
                 query_strings: dict = None, form_params: dict = None,
                 text: str = None):
        self.path = path
        self.method = method
        self.headers = headers
        self.query_strings = query_strings
        self.form_params = form_params
        self.text = text
        parsed_text = self.text.split('\r\n\r\n')
        self.body_text = '\r\n\r\n'.join(parsed_text[1:]) if len(parsed_text) > 1 else ''

    @property
    def body_format(self) -> Union[BodyFormat, None]:
        content_type_raw = CaseInsensitiveDict(self.headers).get('Content-Type', None)
        return {
            BodyFormatJson.header_mime: BodyFormatJson,
            BodyFormatYaml.header_mime: BodyFormatYaml,
            BodyFormatXml.header_mime: BodyFormatXml
        }.get(content_type_raw.split(';', 1)[0], None) if content_type_raw else None

    def __repr__(self):
        return self.text

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


class Response:

    def __init__(self, status: int, headers: dict, body: str):
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
            'body_format': self.body_format.name if self.body_format else None,
            'body_text': self.body
        }

    def repr_headers(self):
        return '\n'.join('%s: %s' % header for header in self.headers.items())

    def __repr__(self):
        return '%s%s' % (
            self.repr_headers(),
            '\r\n\r\n%s' % self.body
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
