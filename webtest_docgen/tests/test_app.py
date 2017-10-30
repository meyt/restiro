import unittest

from webtest_docgen.tests.helpers import WebAppTestCase


class AppTestCase(WebAppTestCase):

    def test_app(self):
        resp = self.wsgi_app.get('/user', 'a=b')
        resp.mustcontain('a=b')

        resp = self.wsgi_app.get('/user', 'b=c')
        resp.mustcontain('b=c')

if __name__ == '__main__':  # pragma: nocover
    unittest.main()
