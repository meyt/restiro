from typing import Union

from urllib.parse import parse_qs

from restiro import DocumentationRoot, ExampleRequest, ResourceExample


class Request:

    def __init__(self, environ):
        self.environ = environ

    @property
    def method(self):
        """`HTTP Request method
        <https://tools.ietf.org/html/rfc7231#section-4.3>`_
        """
        return self.environ['REQUEST_METHOD'].lower()

    @property
    def path(self):
        """Request path
        """
        return self.environ['PATH_INFO']

    @property
    def query(self):
        """Request query string
        """
        return {k: v[0] if len(v) == 1 else v for k, v in parse_qs(
            self.environ['QUERY_STRING'],
            keep_blank_values=True,
            strict_parsing=False
        ).items()}

    @property
    def request_content_length(self) -> Union[int, None]:
        """Request content length
        """
        v = self.environ.get('CONTENT_LENGTH')
        return None if not v or not v.strip() else int(v)

    @property
    def body(self):
        if self.request_content_length is None:
            return

        if self.request_content_length == 0:
            return b''

        fp = self.environ['wsgi.input']
        data = fp.read(self.request_content_length)
        return data

    @property
    def headers(self):
        headers = {
            k: v
            for (k, v) in self.environ.items()
            if isinstance(k, str) and k.startswith('HTTP_')
        }
        return dict(map(
            lambda x: (x[0][len('HTTP_'):].replace('_', '-'), x[1]),
            headers.items()
        ))


class MockServer:

    def __init__(self, docs_root: DocumentationRoot):
        self.docs_root = docs_root

    def find_example(self, environ) -> Union[None, ResourceExample]:
        request = Request(environ)

        resource = self.docs_root.resources.find(
            method=request.method,
            path=(
                request.path[len(self.docs_root.base_uri.path):]
                if self.docs_root.base_uri else
                request.path
            )
        )

        if not resource:
            return

        example_request = ExampleRequest(
            method=request.method,
            path=request.path,
            query_strings=request.query,
            headers=request.headers,
            body=request.body
        )

        for example in resource.examples:
            r = example.request

            if all((
                r.path == example_request.path,
                r.method == example_request.method,
                r.query_strings == example_request.query_strings,
                r.form_params == example_request.form_params,
                r.formatted_body == example_request.formatted_body
            )):
                return example

    def __call__(self, environ, start_response):
        example = self.find_example(environ)

        if not example:
            start_response('404 Example Not Found', [])
            yield b''
            return

        response = example.response
        status = "%s %s" % (response.status, response.reason)
        headers = list(response.headers.items())
        start_response(status, headers)
        yield response.body.encode()
