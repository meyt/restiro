import unittest

from webtest_docgen.tests.helpers import WebAppTestCase, mockup_resources


class AppTestCase(WebAppTestCase):

    def test_app(self):
        # Simple request
        self.wsgi_app.get('/far/away')
        resp_one = self.wsgi_app.get('/user', 'a=b')
        resp_one.mustcontain('a=b')

        # Mockup
        self.docs_root.set_resources(*mockup_resources())

        # Fill examples by request
        self.wsgi_app.get('/user')
        resource = self.docs_root.resources.find(path='/user', method='get')
        self.assertEqual(len(resource.examples), 1)
        self.assertEqual(resource.examples[0].response.status, 200)
        self.assertEqual(resource.examples[0].response.body_format, None)

        # JSON Request
        self.wsgi_app.post_json('/user', {
            'full_name': 'Meyti'
        })
        resource = self.docs_root.resources.find(path='/user', method='post')
        self.assertTrue('Meyti' in resource.examples[0].request.__repr__())
        self.assertTrue('Meyti' in resource.examples[0].response.__repr__())


if __name__ == '__main__':  # pragma: nocover
    unittest.main()
