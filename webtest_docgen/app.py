from webtest import TestApp
from . import ResourceExample, Request, Response, DocumentationRoot
import functools


class TestDocumentApp(TestApp):

    def __init__(self, *args, docs_root: DocumentationRoot, **kwargs):
        self._docs_root = docs_root
        super().__init__(*args, **kwargs)

    def do_request(self, req, status=None, expect_errors=None):
        resource = self._docs_root.resources.find(req.path, str(req.method).lower())

        def get_response(func):
            if resource:
                example_request = Request(
                    path=resource.path,
                    method=resource.method,
                    headers=dict(req.headers),
                    query_strings=dict(req.GET),
                    form_params=dict(req.POST),
                )
                response = func()
                example_response = Response(
                    status=response.status_int,
                    body=response.body,
                    headers=dict(response.headers)
                ) if resource else None

                resource.examples.append(
                    ResourceExample(request=example_request, response=example_response)
                )
                return response
            return func()

        return get_response(
            functools.partial(super().do_request, req=req, status=status, expect_errors=expect_errors)
        )
