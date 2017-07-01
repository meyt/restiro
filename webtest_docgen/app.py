from webtest import TestApp
from . import Resource, DocRoot


class TestDocumentApp(TestApp):
    docs_root = None

    def __init__(self, *args, docs_root: DocRoot, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.docs_root = docs_root

    def post(self, url, params='', headers=None, extra_environ=None,
             status=None, upload_files=None, expect_errors=False,
             content_type=None, xhr=False):
        # TODO get resource by path
        # TODO call super().post
        # TODO get response from super().post
        # TODO set resource and response to document generator
        # TODO return super().post result
        pass
