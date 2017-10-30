import unittest

from webtest_docgen import (
    DocumentationRoot,
    Document,
    Resource,
    FormParam,
    QueryParam,
    UriParam,
    HeaderParam,
    Response
)


class ModelTestCase(unittest.TestCase):

    def test_model(self):
        docs_root = DocumentationRoot(
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

        user_id_param = UriParam(
            name='user_id',
            type_='integer',
            required=True
        )

        user_resource_get = Resource(
            path='/user/me',
            method='get',
            params=HeaderParam(
                name='Authorization'
            )
        )
        self.assertEqual(user_resource_get.__filename__, 'user-me-get')
        self.assertEqual(9, len(user_resource_get.to_dict().keys()))
        self.assertEqual(user_resource_get.__repr__(), 'GET /user/me')

        user_resource_put = Resource(
            path='/user/{user_id}',
            method='put',
            params=user_id_param
        )
        user_resource_patch = Resource(
            path='/user/{user_id}',
            method='patch',
            params=[user_id_param]
        )

        # Append resources
        docs_root.resources.append(user_resource_get)
        docs_root.resources.append(user_resource_put)
        docs_root.resources.append(user_resource_patch)

        # Append documents
        docs_root.documents.append(
            Document(
                title='AnotherDocument',
                content='AnotherDocument Contents!'
            )
        )

        # Add wrong resource
        with self.assertRaises(TypeError):
            docs_root.resources.append('Ha?')

        # Add wrong document
        with self.assertRaises(TypeError):
            docs_root.documents.append('Ha?')

        # Find resource
        self.assertNotEqual(None, docs_root.resources.find('/user', 'get'))
        self.assertEqual(None, docs_root.resources.find('/user/wrong', 'get'))

        # Get resources Tree
        resources_tree = docs_root.resources.__tree__
        self.assertEqual(4, len(resources_tree.keys()))
        self.assertEqual(2, len(resources_tree['/user/{user_id}'].keys()))

    def test_response(self):
        response = Response(
            status=200,
            headers={
                'Authorization': 'Bearer <token>'
            },
            body=b'Welcome'
        )
        self.assertEqual(response.body_format, None)

        with self.assertRaises(Exception):
            _ = response.body_json

        self.assertEqual(4, len(response.to_dict().keys()))

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
