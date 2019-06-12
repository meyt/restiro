import json

from restiro import DocumentationRoot
from restiro.mock_server import MockServer


def mockup_resources():
    from restiro import (
        Resource,
        FormParam,
        QueryParam,
        HeaderParam,
        URLParam,
        ResourceExample,
        ExampleRequest,
        ExampleResponse
    )

    return [
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
                    body=json.dumps({
                        'name': 'John Doe',
                        'age': 18
                    }),
                    headers={
                        'Content-Type': 'application/json'
                    }
                )
            )]
        ),
        Resource(
            path='/user/:user_id',
            method='get',
            description='Get single user',
            params=[URLParam(
                name='user_id',
                type_='integer'
            )],
            examples=[ResourceExample(
                request=ExampleRequest(
                    method='get',
                    path='/user/12'
                ),
                response=ExampleResponse(
                    status=200,
                    reason='OK',
                    body=json.dumps({
                        'name': 'Matt Smith',
                        'age': 18
                    }),
                    headers={
                        'Content-Type': 'application/json'
                    }
                )
            )]
        ),
        Resource(
            path='/user/:user_id/image',
            method='get',
            description='Get user images',
            params=[URLParam(
                name='user_id',
                type_='integer'
            )]
        ),
        Resource(
            path='/user/:user_id/image/:image_id',
            method='get',
            description='Get user image by id',
            params=[
                URLParam(
                    name='user_id',
                    type_='integer'
                ),
                URLParam(
                    name='image_id',
                    type_='integer'
                )
            ]
        ),
        Resource(
            path='/photo',
            method='get',
            description='Get all photos',
            params=[QueryParam(
                name='order',
                type_='string',
                default='date'
            )],
            examples=[
                ResourceExample(
                    request=ExampleRequest(
                        method='get',
                        path='/photo'
                    ),
                    response=ExampleResponse(
                        status=401,
                        reason='Not Authorized',
                        headers={},
                        body=''
                    )
                ),
                ResourceExample(
                    request=ExampleRequest(
                        method='get',
                        path='/photo',
                        query_strings={'sort': 'title'}
                    ),
                    response=ExampleResponse(
                        status=200,
                        reason='OK',
                        headers={'content-type': 'application/json'},
                        body=json.dumps(['photo A', 'photo B'])
                    )
                )
            ]
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
            ],
            examples=[
                ResourceExample(
                    request=ExampleRequest(
                        method='post',
                        path='/user',
                        body=json.dumps({'name': 'Ella', 'age': 16})
                    ),
                    response=ExampleResponse(
                        status=200,
                        reason='OK',
                        headers={'content-type': 'application/json'},
                        body=json.dumps({'name': 'Ella', 'age': 16})
                    )
                )
            ]
        ),
        Resource(
            path='/user/:userId',
            method='delete',
            description='Delete a user',
            examples=[ResourceExample(
                request=ExampleRequest(
                    method='delete',
                    path='/user/10'
                ),
                response=ExampleResponse(
                    status=204,
                    reason='No Content',
                    headers={},
                    body=''
                )
            )]
        ),
    ]


def test_mock_server():
    from webtest import TestApp

    # Initiate documentation root
    docs_root = DocumentationRoot(
        title='Hello World'
    )
    docs_root.resources.extend(mockup_resources())

    mock_server = MockServer(docs_root)
    app = TestApp(app=mock_server)

    # Simple get
    resp = app.get('/user')
    assert resp.status == '200 OK'
    assert resp.json['name'] == 'John Doe'

    # URL parameter
    resp = app.get('/user/12')
    assert resp.status == '200 OK'
    assert resp.json['name'] == 'Matt Smith'

    # Not 2xx status
    resp = app.get('/photo', status=401)
    assert resp.status == '401 Not Authorized'

    # Query string
    resp = app.get('/photo?sort=title')
    assert resp.status == '200 OK'
    assert resp.json == ['photo A', 'photo B']

    # Query string with different value must return similar resource
    resp = app.get('/photo?sort=url')
    assert resp.status == '200 OK'
    assert resp.json == ['photo A', 'photo B']

    # No content
    resp = app.delete('/user/10', status=204)
    assert resp.status == '204 No Content'

    # JSON post with parameters
    resp = app.post_json('/user', params={'name': 'Ella', 'age': 16})
    assert resp.status == '200 OK'
    assert resp.json['name'] == 'Ella'
    assert resp.json['age'] == 16

    # JSON post with different parameter values must return similar resource
    resp = app.post_json('/user', params={'name': 'Bella', 'age': 16})
    assert resp.status == '200 OK'
    assert resp.json['name'] == 'Ella'
    assert resp.json['age'] == 16

    resp = app.options('/user', status=404)
    assert resp.status == '404 Example Not Found'
