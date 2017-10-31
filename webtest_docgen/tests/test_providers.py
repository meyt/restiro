import unittest

from webtest_docgen import MarkdownProvider, JSONProvider
from webtest_docgen.tests.helpers import WebAppProviderTestCase


class ProvidersTestCase(WebAppProviderTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()
        from webtest_docgen.tests.helpers import mockup_app_tests
        mockup_app_tests(self.wsgi_app)

    def test_markdown_provider(self):
        provider = MarkdownProvider(
            docs_root=self.docs_root,
            destination_dir=self.get_destination_dir('markdown')
        )
        provider.generate()

    def test_json_provider(self):
        provider = JSONProvider(
            docs_root=self.docs_root,
            destination_dir=self.get_destination_dir('json')
        )
        provider.generate()

if __name__ == '__main__':  # pragma: nocover
    unittest.main()
