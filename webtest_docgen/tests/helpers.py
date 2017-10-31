import unittest
import shutil
from os import makedirs
from os.path import join, dirname, abspath, exists

from webtest.debugapp import debug_app

from webtest_docgen import (
    TestDocumentApp,
    DocumentationRoot,
    Document,
    Resource,
    FormParam,
    QueryParam
)


def mockup_doc_root():
    return DocumentationRoot(
        title='My App',
        version='1',
        base_uri='http://localhost/api/v1',
        documents=[
            Document(
                title='HeaderOne',
                content='This is content of HeaderOne.'
            )
        ],
        resources=[
            Resource(
                path='/user',
                method='get',
                description='Get all users'
            ),
            Resource(
                path='/photo',
                method='get',
                description='Get all photos',
                params=QueryParam(
                    name='order',
                    type_='string',
                    default='date'
                )
            ),
            Resource(
                path='/user',
                method='post',
                description='Create a new user',
                params=[
                    FormParam(
                        name='full_name',
                        type_='string',
                        required=True
                    ),
                    FormParam(
                        name='avatar',
                        type_='file'
                    )
                ]
            ),
        ]
    )


def mockup_app_tests(wsgi_app):
    wsgi_app.get('/user', 'a=b')
    wsgi_app.get('/user', 'b=c')


class WebAppTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.this_dir = abspath(join(dirname(__file__), '.'))
        cls.stuff_path = join(cls.this_dir, 'stuff')
        cls.temp_path = join(cls.this_dir, 'stuff', 'temp')

        # Remove previous files, if any! to make a clean temp directory:
        if exists(cls.temp_path):  # pragma: no cover
            shutil.rmtree(cls.temp_path)

        makedirs(cls.temp_path)

    def setUp(self):
        super().setUp()
        self.docs_root = mockup_doc_root()
        self.wsgi_app = TestDocumentApp(
            app=debug_app,
            docs_root=self.docs_root
        )


class WebAppProviderTestCase(WebAppTestCase):

    def get_destination_dir(self, provider_name):
        result = join(self.temp_path, '%s_provider' % provider_name)
        makedirs(result)
        return result
