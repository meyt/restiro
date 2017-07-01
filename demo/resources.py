from webtest_docgen import (
    DocRoot,
    Doc,
    Resource,
    Param,
    UriParam,
    HeaderParam,
    FormParam,
    QueryParam
)


docs_root = DocRoot(
    title='My App',
    version='1',
    base_uri='http://localhost/api/v1'
)

docs_root.documentation.append(
    Doc(
        title='HeaderOne',
        content='Hello World'
    )
)

docs_root.resources.append(
    Resource(
        path='/register',
        method='post'
    ).set_params(
        FormParam(
            name='full_name',
            type_='Text',
            default='Hello',
            required=True
        ),
        FormParam(
            name='avatar',
            type_='file',
            default='hello'
        )
    ),
    Resource(
        path='/users/{user_id}',
        method='get'
    ).set_params(
        QueryParam(
            name='orderby',
            display_name='',
            default='created_at',
            enum=[
                'created_at',
                'full_name',
                'birthday'
            ],
            type_='string'
        )
    ),
    Resource(

    )
)
