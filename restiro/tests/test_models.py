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
    BodyFormatJson
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

    user_id_param = URLParam(
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
    assert user_resource_get.__filename__ == 'user-me-get'
    assert len(user_resource_get.to_dict().keys()) == 9
    assert user_resource_get.__repr__() == 'GET /user/me'

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

    # Single resource
    DocumentationRoot(
        title='My App2',
        resources=user_resource_get,
        documents=Document(
            title='Welcome',
            content='Welcome to my second app.'
        )
    )

    # Params generator
    def params_generator():
        yield HeaderParam(
            name='Authorization',
            type_='string'
        )
        yield QueryParam(
            name='sort',
            type_='string'
        )

    docs_root_app3 = DocumentationRoot(
        title='My App3',
        resources=Resource(
            path='/news',
            method='get',
            params=params_generator()
        )
    )
    docs_root_app3_dict = docs_root_app3.to_dict()
    assert len(docs_root_app3_dict['resources'][0]['header_params']) == 1
    assert len(docs_root_app3_dict['resources'][0]['query_params']) == 1

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
    assert len(resources_tree['/user/{user_id}'].keys()) == 2


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


def test_response():
    response_example = ExampleResponse(
        status=200,
        headers={
            'Authorization': 'Bearer <token>'
        },
        body='Welcome'
    )
    assert response_example.body_format is None

    _ = response_example.body_json

    assert len(response_example.to_dict().keys()) == 4

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
