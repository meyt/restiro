
from os.path import join
from uuid import uuid4
from urllib.parse import parse_qs

from webtest import TestApp as WebtestApp

from restiro import (
    ResourceExample,
    ExampleRequest,
    ExampleResponse
)
from restiro.helpers import get_examples_dir


def parse_query_string(qs):
    return {k: v[0] if len(v) == 1 else v for k, v in parse_qs(
        qs,
        keep_blank_values=True,
        strict_parsing=False
    ).items()}


class TestApp(WebtestApp):

    def __init__(self, *args, examples_dir: str=None, **kwargs):
        self._examples_dir = examples_dir or get_examples_dir()
        self.doc = False
        self.force_doc = False
        self.requests_index = 0
        super().__init__(*args, **kwargs)

    def do_request(self, req, status=None, expect_errors=None):
        self.requests_index += 1

        # Exclude binary body
        try:
            request_body = req.body.decode()
        except UnicodeDecodeError:
            request_body = None

        # Fill example
        example_request = ExampleRequest(
            path=str(req.path),
            method=str(req.method).lower(),
            headers=dict(req.headers),
            body=request_body,
            query_strings=parse_query_string(req.query_string),
            form_params=dict(req.POST) if isinstance(req.POST, dict) else None)

        response = super().do_request(
            req=req,
            status=status,
            expect_errors=expect_errors)

        try:
            response_body = str(response.text)
        except UnicodeDecodeError:
            response_body = None

        example_response = ExampleResponse(
            status=response.status_int,
            body=response_body,
            headers=dict(response.headers),
            reason=response.status[3:].strip())

        example_filename = join(
            self._examples_dir,
            '%s-%s.json' % (self.requests_index, uuid4().hex))

        ResourceExample(
            request=example_request,
            response=example_response,
            visible=any((self.doc, self.force_doc))
        ).dump(
            example_filename
        )

        self.doc = False

        if req.method != 'OPTIONS':
            super().options(url=req.path)

        return response
