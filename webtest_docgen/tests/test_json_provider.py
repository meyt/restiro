import unittest

from webtest_docgen import JSONProvider
from webtest_docgen.tests.helpers import WebAppProviderTestCase


class JSONProviderTestCase(WebAppProviderTestCase):

    def test_json_provider(self):
        from webtest_docgen.tests.helpers import mockup_app_tests
        mockup_app_tests(self.wsgi_app)

        provider = JSONProvider(
            docs_root=self.docs_root,
            destination_dir=self.get_destination_dir('json')
        )
        provider.generate()

if __name__ == '__main__':  # pragma: nocover
    unittest.main()
