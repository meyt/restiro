from os.path import join, dirname, abspath

this_dir = abspath(join(dirname(__file__), '.'))
package_dir = dirname(dirname(this_dir))
stuff_dir = join(this_dir, 'stuff')
temp_dir = join(package_dir, 'temp')


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
            description='Get all users'
        ),
        Resource(
            path='/user/:user_id',
            method='get',
            description='Get single user',
            params=[URLParam(
                name='user_id',
                type_='integer'
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
                        status=200,
                        reason='OK',
                        headers={'Authorization': 'bla'},
                        body=''
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
            ]
        ),
    ]


def mockup_documents():
    from restiro import Document
    return [
        Document(
            title='HeaderOne',
            content='This is content of HeaderOne.'
        )
    ]


def mockup_doc_root():
    from restiro import DocumentationRoot
    return DocumentationRoot(
        title='My App',
        base_uri='http://localhost/api/v1',
        documents=mockup_documents(),
        resources=mockup_resources()
    )
