
from restiro.models import (
    DocumentationRoot,
    Document,
    Resource,
    FormParam,
    QueryParam
)


def test_translations():
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
    translations = docs_root.extract_translations()
    assert len(translations) == 6
    assert 'My App' in translations
    assert 'HeaderOne' in translations
    assert 'This is content of HeaderOne.' in translations
    assert 'Get all users' in translations
    assert 'Get all photos' in translations
    assert 'Create a new user' in translations
