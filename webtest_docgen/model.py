"""
    Resources model based on RAML 0.8
"""


class DocRoot:
    title = None
    version = None
    base_uri = None
    media_type = None
    protocols = []
    documentation = []
    base_uri_params = []
    resources = Resources()

    def __init__(self, title=None, version=None,
                 base_uri=None, protocols=None, media_type=None):
        for key, value in locals():
            setattr(self, key, value)

    def set_resources(self, *args):
        for item in args:
            self.resources.append(item)

    def set_docs(self, *args):
        for item in args:
            self.resources.append(item)


class Doc:
    title = None
    content = None

    def __init__(self, title=None, content=None):
        self.title, self.content = title, content


class Resources(dict):

    def append(self, item):
        if isinstance(item, list):
            for item_ in item:
                self.append(item_)
        else:
            if not isinstance(item, Resource):
                raise TypeError('item is not of type Resource')
            self.update({item.path: item})


class Resource:
    path = None
    method = None
    display_name = None
    description = None
    uri_params = []
    query_params = []
    form_params = []
    header_params = []

    def __init__(self, path=None, method=None, display_name=None, description=None):
        for key, value in locals():
            setattr(self, key, value)

    def set_params(self, *args):
        for item in args:
            if isinstance(item, UriParam):
                self.uri_params.append(item)

            elif isinstance(item, QueryParam):
                self.query_params.append(item)

            elif isinstance(item, FormParam):
                self.form_params.append(item)

            elif isinstance(item, HeaderParam):
                self.header_params.append(item)


class Param:
    name = None
    display_name = None
    description = None
    type_ = None
    enum = None
    pattern = None
    min_length = None
    max_length = None
    minimum = None
    maximum = None
    example = None
    repeat = None
    required = None
    default = None
    media_type = None

    def __init__(self, name=None, display_name=None, description=None, type_=None, enum=None,
                 pattern=None, min_length=None, max_length=None, minimum=None, maximum=None,
                 example=None, repeat=None, required=None, default=None, media_type=None):
        for key, value in locals():
            setattr(self, key, value)


class UriParam(Param):
    pass


class QueryParam(Param):
    pass


class FormParam(Param):
    pass


class HeaderParam(Param):
    pass
