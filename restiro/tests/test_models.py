import pytest

from restiro.models import (
    DocumentationRoot,
    Document,
    Resource,
    FormParam,
    QueryParam,
    URLParam,
    HeaderParam,
    ExampleResponse,
    BodyFormatJson,
    ResourceExample,
    ExampleRequest
)


def test_model():
    docs_root = DocumentationRoot(
        title='My App',
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
                description='Get all users',
                examples=[ResourceExample(
                    request=ExampleRequest(
                        method='get',
                        path='/user'
                    ),
                    response=ExampleResponse(
                        status=200,
                        reason='OK',
                        headers={},
                        body=''
                    )
                )]
            ),
            Resource(
                path='/photo',
                method='get',
                description='Get all photos',
                params=[QueryParam(
                    name='order',
                    type_='string',
                    default='date'
                )]
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

    user_resource_get = Resource(
        path='/user/me',
        method='get',
        params=[
            HeaderParam(
                name='Authorization'
            )
        ]
    )

    assert user_resource_get.__filename__ == 'user-me-get'
    assert len(user_resource_get.to_dict().keys()) == 11
    assert user_resource_get.__repr__() == 'GET /user/me'

    # Append resources
    docs_root.resources.append(user_resource_get)
    docs_root.resources.append(
        Resource(
            path='/user/:user_id',
            method='put',
            params=[
                URLParam(
                    name='user_id',
                    type_='integer',
                    required=True
                )
            ]
        )
    )
    docs_root.resources.append(
        Resource(
            path='/user/:user_id',
            method='patch',
            params=[
                URLParam(
                    name='user_id',
                    type_='integer',
                    required=True
                )
            ]
        )
    )

    # Append documents
    docs_root.documents.append(
        Document(
            title='AnotherDocument',
            content='AnotherDocument Contents!'
        )
    )

    # Add wrong resource
    with pytest.raises(TypeError):
        docs_root.resources.append('Ha?')

    # Add wrong document
    with pytest.raises(TypeError):
        docs_root.documents.append('Ha?')

    # Find resource
    assert docs_root.resources.find('/user', 'get') is not None
    assert docs_root.resources.find('/user/wrong', 'get') is None

    # Get resources Tree
    resources_tree = docs_root.resources.__tree__
    assert len(resources_tree.keys()) == 4
    assert len(resources_tree['/user/:user_id'].keys()) == 2

    # Export/Import models
    root_dict = docs_root.to_dict()
    new_docs_root = DocumentationRoot.create_from_dict(root_dict)
    assert root_dict == new_docs_root.to_dict()

    resource = new_docs_root.resources.find(method='get', path='/user')
    assert isinstance(resource, Resource)
    assert isinstance(resource.examples[0], ResourceExample)


def test_parameter_python_type():
    import decimal
    import datetime
    resource = Resource(
        path='/',
        method='get',
        params=[
            FormParam(
                name='p1',
                type_=decimal.Decimal
            ),
            FormParam(
                name='p2',
                type_='file'
            ),
            FormParam(
                name='p3',
                type_=datetime
            )
        ]
    ).to_dict()
    assert resource['form_params'][0]['type'] == 'number'
    assert resource['form_params'][1]['type'] == 'file'
    assert resource['form_params'][2]['type'] == 'date'


def test_resource_example():
    resource_example = ResourceExample(
        request=ExampleRequest(
            method='POST',
            path='/bla/bla',
            headers={
                'Authorization': 'Bearer <token>'
            }
        ),
        response=ExampleResponse(
            status=200,
            headers={
                'Authorization': 'Bearer <token>'
            },
            body='Welcome'
        )
    )
    assert resource_example.response.body_format is None

    _ = resource_example.response.body_json

    assert len(resource_example.response.to_dict().keys()) == 5
    assert len(resource_example.to_dict().keys()) == 3

    # Check body format recognize
    response_example = ExampleResponse(
        status=200,
        headers={
            'Content-Length': len(b'Welcome'),
            'Content-Type': 'application/json; charset=utf-8'
        },
        body='Welcome'
    )
    assert response_example.body_format == BodyFormatJson

    # Represent example request
    assert resource_example.request.__repr__() == '''POST /bla/bla

authorization: Bearer <token>'''

    # Export/Import
    example_dict = resource_example.to_dict()
    new_example = resource_example.create_from_dict(example_dict)
    assert example_dict == new_example.to_dict()
