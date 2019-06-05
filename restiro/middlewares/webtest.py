
from os.path import join
from uuid import uuid4

from webtest import TestApp as WebtestApp

from restiro import (
    ResourceExample,
    ExampleRequest,
    ExampleResponse
)
from restiro.helpers import get_examples_dir


class TestApp(WebtestApp):

    def __init__(self, *args, examples_dir: str=None, **kwargs):
        self._examples_dir = examples_dir or get_examples_dir()
        self.doc = False
        self.force_doc = False
        self.requests_index = 0
        super().__init__(*args, **kwargs)

    def do_request(self, req, status=None, expect_errors=None):
        if not self.doc and not self.force_doc:
            return super().do_request(req=req, status=status,
                                      expect_errors=expect_errors)

        self.doc = False
        self.requests_index += 1

        # Fill example
        example_request = ExampleRequest(
            path=str(req.path),
            method=str(req.method).lower(),
            headers=dict(req.headers),
            body=req.body.decode(),
            query_strings=dict(req.GET),
            form_params=dict(req.POST))

        response = super().do_request(
            req=req,
            status=status,
            expect_errors=expect_errors)

        example_response = ExampleResponse(
            status=response.status_int,
            body=str(response.text),
            headers=dict(response.headers),
            reason=response.status[3:].strip())

        example_filename = join(
            self._examples_dir,
            '%s-%s.pickle' % (self.requests_index, uuid4().hex))

        ResourceExample(
            request=example_request,
            response=example_response
        ).dump(
            example_filename
        )

        return response
