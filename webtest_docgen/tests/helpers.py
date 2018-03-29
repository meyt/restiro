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
    QueryParam,
    HeaderParam,
    UriParam
)


def mockup_resources():
    return [
        Resource(
            path='/user',
            method='get',
            description='Get all users'
        ),
        Resource(
            path='/user/{user_id}',
            method='get',
            description='Get single user',
            params=UriParam(
                name='user_id',
                type_='integer'
            )
        ),
        Resource(
            path='/user/{user_id}/image',
            method='get',
            description='Get user images',
            params=UriParam(
                name='user_id',
                type_='integer'
            )
        ),
        Resource(
            path='/user/{user_id}/image/{image_id}',
            method='get',
            description='Get user image by id',
            params=[
                UriParam(
                    name='user_id',
                    type_='integer'
                ),
                UriParam(
                    name='image_id',
                    type_='integer'
                )
            ]
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
                ),
                HeaderParam(
                    name='Authorization',
                    type_='str'
                )
            ]
        ),
    ]


def mockup_documents():
    return [
        Document(
            title='HeaderOne',
            content='This is content of HeaderOne.'
        )
    ]


def mockup_doc_root():
    return DocumentationRoot(
        title='My App',
        version='1',
        base_uri='http://localhost/api/v1',
        documents=mockup_documents(),
        resources=mockup_resources()
    )


def mockup_app_tests(wsgi_app):
    wsgi_app.get('/user', 'a=b')
    wsgi_app.get('/user', 'b=c')
    wsgi_app.post('/user', params={
        'full_name': 'Lily'
    })


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
