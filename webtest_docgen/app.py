from webtest import TestApp
from . import ResourceExample, Request, ExampleResponse, DocumentationRoot
import functools


class TestDocumentApp(TestApp):

    def __init__(self, *args, docs_root: DocumentationRoot, **kwargs):
        self._docs_root = docs_root
        super().__init__(*args, **kwargs)

    def do_request(self, req, status=None, expect_errors=None):
        resources_method = str(req.method).lower()
        resource_path = str(req.path)
        resource = self._docs_root.resources.find(resource_path,
                                                  resources_method)
        if not resource:
            resource_path = resource_path[len(self._docs_root.base_uri_path):]
            resource = self._docs_root.resources.find(resource_path,
                                                      resources_method)

        def get_response(func):
            if resource:
                example_request = Request(
                    path=resource.path,
                    method=resource.method,
                    headers=dict(req.headers),
                    text=str(req.as_text()),
                    query_strings=dict(req.GET),
                    form_params=dict(req.POST),
                )
                response = func()
                example_response = ExampleResponse(
                    status=response.status_int,
                    body=str(response.body),
                    headers=dict(response.headers)
                )

                resource.examples.append(
                    ResourceExample(request=example_request,
                                    response=example_response)
                )
                return response
            return func()

        return get_response(
            functools.partial(super().do_request, req=req, status=status,
                              expect_errors=expect_errors)
        )
