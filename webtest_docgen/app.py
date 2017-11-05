from webtest import TestApp
from . import ResourceExample, Request, Response, DocumentationRoot


class TestDocumentApp(TestApp):

    def __init__(self, *args, docs_root: DocumentationRoot, **kwargs):
        self._docs_root = docs_root
        super().__init__(*args, **kwargs)

    def do_request(self, req, status=None, expect_errors=None):
        resource = self._docs_root.resources.find(req.path, str(req.method).lower())
        response = super().do_request(req, status=status, expect_errors=expect_errors)

        if resource:
            example_request = Request(
                path=resource.path,
                method=resource.method,
                headers=dict(req.headers),
                query_strings=dict(req.GET),
                form_params=dict(req.POST),
            )
            example_response = Response(
                status=response.status,
                body=response.body,
                headers=dict(response.headers)
            )
            resource.examples.append(
                ResourceExample(request=example_request, response=example_response)
            )

        return response
