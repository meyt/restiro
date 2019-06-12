from typing import List, Union, Tuple

from .parameters import URLParam, FormParam, HeaderParam, QueryParam, Param
from .example import ResourceExample
from .translation_mixin import TranslationMixin


class Resource(TranslationMixin):
    __translation_keys__ = (
        'description',
        'display_name'
    )

    def __init__(self, path: str, method: str, display_name: str = None,
                 description: str = None, tags: List[str] = None,
                 params: List[Param] = None,
                 security: dict = None,
                 examples: List[ResourceExample] = None):
        """
        Resource
        :param path: The URI relative to the `DocumentationRoot.base_uri` and 
                     MUST begin with a slash (/).
                     .. seealso:: :class:`.DocumentationRoot`
        :param method: The method of resource. In a RESTful API, methods are
                       operations that are performed on a resource.
                       A method MUST be one of the HTTP methods defined in
                       the HTTP version 1.1 specification [RFC2616] and its
                       extension, RFC5789 [RFC5789].
        :param display_name: The displayName attribute provides a friendly name
                             to the resource and can be used by documentation
                             generation tools.
        :param description: The description property that briefly describes
                            the resource. It is RECOMMENDED that all the API
                            definition's resources includes the description
                            property.
        :param params: Collection of parameters (Include any inheritance
                       of `Param`)
        :param security: Collection of permissions
        :param examples: Collection of examples
        """
        self.path = path
        self.method = method
        self.display_name = display_name
        self.description = description
        self.tags = tags
        self.uri_params = []
        self.query_params = []
        self.form_params = []
        self.security = security
        self.header_params = []
        self.examples = examples if examples else []

        if params:
            self.set_params(*params)

    def set_params(self, *args):
        for item in args:
            if isinstance(item, URLParam):
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
            'tags': self.tags,
            'security': self.security,
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

    def extract_translations(self):
        result = super().extract_translations()
        for param in self.params:
            result.extend(param.extract_translations())
        return result

    @classmethod
    def create_from_dict(cls, data: dict) -> 'Resource':
        params = []
        params_map = (
            ('header_params', HeaderParam),
            ('uri_params', URLParam),
            ('query_params', QueryParam),
            ('form_params', FormParam)
        )
        for key, type_class in params_map:
            for param_data in data[key]:
                params.append(type_class.create_from_dict(param_data))

        examples = [
            ResourceExample.create_from_dict(o) for o in data['examples']
        ]

        return cls(
            path=data['path'],
            method=data['method'],
            tags=data['tags'],
            security=data['security'],
            display_name=data['display_name'],
            description=data['description'],
            examples=examples,
            params=params
        )


class Resources(object):

    def __init__(self):
        self._items = dict()

    def extend(self, items: Union[Tuple[Resource], List[Resource]]):
        for item in items:
            self.append(item)

    def append(self, resource: Resource):
        if not isinstance(resource, Resource):
            raise TypeError('item is not of type Resource')

        original_resource = resource.to_dict()
        original_resource['method'] = 'options'
        original_resource['examples'] = []
        original_resource['params'] = []
        cors_resource = Resource.create_from_dict(original_resource)

        if cors_resource.__key__ not in self._items:
            self._items[cors_resource.__key__] = cors_resource

        self._items[resource.__key__] = resource

    def find(self, path, method) -> Resource:

        if path.endswith('/'):
            path = path[:-1]

        input_path_parts = path[1:].split('/')
        filtered_resources = [
            x for x in self._items.values()
            if (
                x.method == method and
                len(x.path[1:].split('/')) == len(input_path_parts)
            )
        ]

        def _route(resources, part_index=0):
            matched_resources = []
            for resource in resources:
                resource_path_parts = resource.path[1:].split('/')
                if (
                    input_path_parts[part_index] ==
                        resource_path_parts[part_index] or
                        resource_path_parts[part_index][:1] == ':'
                ):
                    matched_resources.append(resource)

            if part_index == len(input_path_parts) - 1:
                return matched_resources[0] if matched_resources else None

            return _route(matched_resources, part_index + 1)

        return _route(resources=filtered_resources)

    @property
    def __tree__(self):
        """
        Get tree of resources
        First level: resource
        Second level: method
        :return: 
        """
        result = {}
        for resource_key, resource in self._items.items():
            result.setdefault(resource.path, {})
            result[resource.path].setdefault(resource.method, [])
            result[resource.path][resource.method].append(resource)
        return result

    def to_dict(self):
        return [resource.to_dict() for _, resource in self._items.items()]

    def extract_translations(self):
        result = []
        for resource in self._items.values():
            result.extend(resource.extract_translations())
        return result

    def translate(self, translator):
        for resource in self._items.values():
            resource.translate(translator)

    def __len__(self):
        return self._items.__len__()

    def items(self):
        return self._items.items()

    def __getitem__(self, item):
        return self._items.__getitem__(item)

    def update(self, obj: 'Resources'):
        self._items.update(obj._items)
