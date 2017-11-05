from typing import List, Union
from .parameters import UriParam, FormParam, HeaderParam, QueryParam, Param


class Resource:

    def __init__(self, path: str, method: str, display_name: str=None,
                 description: str=None, params: Union[Param, List[Param]]=None):
        """
        Resource
        :param path: The URI relative to the `DocumentationRoot.base_uri` and 
                     MUST begin with a slash (/).
                     .. seealso:: :class:`.DocumentationRoot`
        :param method: The method of resource. In a RESTful API, methods are operations that 
                       are performed on a resource. A method MUST be one of the HTTP methods defined in 
                       the HTTP version 1.1 specification [RFC2616] and its extension, RFC5789 [RFC5789].
        :param display_name: The displayName attribute provides a friendly name to 
                             the resource and can be used by documentation generation tools.
        :param description: The description property that briefly describes the resource. 
                            It is RECOMMENDED that all the API definition's resources 
                            includes the description property.
        :param params: Collection of parameters (Include any inheritance of `Param`)
        """
        self.path = path
        self.method = method
        self.display_name = display_name
        self.description = description
        self.uri_params = []
        self.query_params = []
        self.form_params = []
        self.header_params = []
        self.examples = []

        if params:
            if isinstance(params, list):
                self.set_params(*params)
            else:
                self.set_params(params)

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
        return self

    @property
    def params(self):
        """ List of all parameters """
        return (
            self.uri_params +
            self.query_params +
            self.header_params +
            self.form_params
        )

    @property
    def __key__(self):
        return '%s-%s' % (self.path, self.method)

    @property
    def __filename__(self):
        return str(self.__key__).lstrip('/').replace('/', '-')

    def to_dict(self):
        return {
            'path': self.path,
            'method': self.method,
            'display_name': self.display_name,
            'description': self.description,
            'header_params': [param.to_dict() for param in self.header_params],
            'uri_params': [param.to_dict() for param in self.uri_params],
            'query_params': [param.to_dict() for param in self.query_params],
            'form_params': [param.to_dict() for param in self.form_params],
            'examples': [example.to_dict() for example in self.examples]
        }

    def __repr__(self):
        return '%s %s' % (self.method.upper(), self.path)


class Resources(dict):

    def append(self, resource: Resource):
        if not isinstance(resource, Resource):
            raise TypeError('item is not of type Resource')
        self[resource.__key__] = resource

    def find(self, path, method) -> Resource:
        return self.get('%s-%s' % (path, method), None)

    @property
    def __tree__(self):
        """
        Get tree of resources
        First level: resource
        Second level: method
        :return: 
        """
        result = {}
        for resource_key, resource in self.items():
            result.setdefault(resource.path, {})
            result[resource.path].setdefault(resource.method, [])
            result[resource.path][resource.method].append(resource)
        return result

    def to_dict(self):
        return [resource.to_dict() for resource_key, resource in self.items()]
