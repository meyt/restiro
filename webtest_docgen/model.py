"""
    Resources model based on RAML 0.8
"""
import json
from typing import Union

from webtest_docgen.utils import to_snake_case, replace_non_alphabet


class Document:

    def __init__(self, title, content=None):
        self.title, self.content = title, content

    @property
    def __filename__(self):
        return replace_non_alphabet(to_snake_case(self.title), '-')

    def to_dict(self):
        return {
            'title': self.title,
            'content': self.content
        }


class BodyFormat:
    name = None
    header_mime = None


class BodyFormatJson(BodyFormat):
    name = 'json'
    header_mime = 'application/json'


class BodyFormatXml(BodyFormat):
    name = 'xml'
    header_mime = 'application/xml'


class BodyFormatYaml(BodyFormat):
    name = 'yaml'
    header_mime = 'application/x-yaml'


class Resource:

    def __init__(self, path: str, method: str, display_name: str=None,
                 description: str=None, params=None):
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
            if isinstance(params, (list, tuple)):
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


class Request:
    def __init__(self, path, method, headers=None,
                 query_strings=None, form_params=None):
        self.path = path
        self.method = method
        self.headers = headers
        self.query_strings = query_strings
        self.form_params = form_params

    def __repr__(self):
        result = '%s %s' % (self.method.upper(), self.path)
        if self.headers:
            result += '\n%s' % '\n'.join('%s: %s' % header for header in self.headers.items())

        if self.form_params:
            result += '\n\n%s' % '\n'.join('%s: %s' % param for param in self.form_params.items())

        return result

    def to_dict(self):
        return {
            'path': self.path,
            'method': self.method,
            'headers': dict(self.headers) if self.headers else None,
            'query_strings': dict(self.query_strings) if self.query_strings else None,
            'form_params': self.form_params if self.form_params else None
        }


class Response:

    def __init__(self, status: int, headers: dict, body: bytes):
        self.status = status
        self.headers = headers
        self.body = body

    @property
    def body_format(self) -> Union[BodyFormat, None]:
        content_type_raw = self.headers.get('Content-type', None)
        return {
            BodyFormatJson.header_mime: BodyFormatJson,
            BodyFormatYaml.header_mime: BodyFormatYaml,
            BodyFormatXml.header_mime: BodyFormatXml
        }.get(content_type_raw.split(';', 1)[0], None) if content_type_raw else None

    @property
    def body_json(self):
        return json.loads(self.body)

    def to_dict(self):
        return {
            'status': self.status,
            'headers': dict(self.headers),
            'body': self.body.decode(),
            'body_format': self.body_format.name if self.body_format else None
        }

    def __repr__(self):
        return '%s%s' % (
            '%s' % '\n'.join('%s: %s' % header for header in self.headers.items()),
            '\n\n%s' % self.body
        )


class ResourceExample:
    def __init__(self, request: Request, response: Response):
        self.request = request
        self.response = response

    def to_dict(self):
        return {
            'request': self.request.to_dict(),
            'response': self.response.to_dict()
        }


class Param:
    def __init__(self, name=None, display_name=None, description=None, type_=None, enum=None,
                 pattern=None, min_length=None, max_length=None, minimum=None, maximum=None,
                 example=None, repeat=None, required=None, default=None):
        """
        Parameters base class
        
        :param name: Parameter name
        :param display_name: The displayName attribute specifies the parameter's display name. 
                             It is a friendly name used only for display or documentation purposes. 
                             If displayName is not specified, it defaults to the property's key 
                             (the name of the property itself).
        :param description: The description attribute describes the intended use or meaning of the parameter. 
                            This value MAY be formatted using Markdown [MARKDOWN].
        :param type_: The type attribute specifies the primitive 
                      type of the parameter's resolved value. API clients MUST return/throw an error 
                      if the parameter's resolved value does not match the specified type.
                      If type is not specified, it defaults to string. Valid types are:
                      string    Value MUST be a string.
                      number    Value MUST be a number.
                      integer   Value MUST be an integer. 
                                Floating point numbers are not allowed. 
                                The integer type is a subset of the number type.
                      date      Value MUST be a string representation of a date as defined 
                                in RFC2616 Section 3.3 [RFC2616].
                                As defined in [RFC2616], all date/time stamps are represented in 
                                Greenwich Mean Time (GMT), which for the purposes of HTTP is equal 
                                to UTC (Coordinated Universal Time). This is indicated by including 
                                "GMT" as the three-letter abbreviation for the timezone. 
                                Example: Sun, 06 Nov 1994 08:49:37 GMT.
                      boolean   Value MUST be either the string "true" or "false" (without the quotes).
                      file      (Applicable only to Form properties)
                                Value is a file. Client generators SHOULD use 
                                this type to handle file uploads correctly.
        :param enum: The enum attribute provides an enumeration of the parameter's valid values.
                     This MUST be an array. 
                     If the enum attribute is defined, API clients and servers MUST verify 
                     that a parameter's value matches a value in the enum array. 
                     If there is no matching value, the clients and servers MUST treat this as an error.
                     (Applicable only for parameters of type string) 
        :param pattern: The enum attribute provides an enumeration of the parameter's valid values. 
                        This MUST be an array. If the enum attribute is defined, 
                        API clients and servers MUST verify that a parameter's value matches a value 
                        in the enum array. If there is no matching value, the clients and servers MUST 
                        treat this as an error. (Applicable only for parameters of type string) 
        :param min_length: The minLength attribute specifies the parameter value's 
                           minimum number of characters. (Applicable only for parameters of type string) 
        :param max_length: The maxLength attribute specifies the parameter value's 
                           maximum number of characters.(Applicable only for parameters of type string) 
        :param minimum: The minimum attribute specifies the parameter's minimum value.
                        (Applicable only for parameters of type number or integer) 
        :param maximum: The maximum attribute specifies the parameter's maximum value.
                        (Applicable only for parameters of type number or integer) 
        :param example: The example attribute shows an example value for the property. This can be used, 
                        e.g., by documentation generators to generate sample values for the property.
        :param repeat: The repeat attribute specifies that the parameter can be repeated. 
                       If the parameter can be used multiple times, 
                       the repeat parameter value MUST be set to 'true'. 
                       Otherwise, the default value is 'false' and the parameter may not be repeated.
        :param required: The required attribute specifies whether the parameter and its value 
                         MUST be present in the API definition. 
                         It must be either 'true' if the value MUST be present or 'false' otherwise.
                         In general, parameters are optional unless the required attribute 
                         is included and its value set to 'true'.
                         For a URI parameter, the required attribute MAY be omitted, 
                         but its default value is 'true'.
        :param default: The default attribute specifies the default value to use for the property 
                        if the property is omitted or its value is not specified. 
                        This SHOULD NOT be interpreted as a requirement for the client to send 
                        the default attribute's value if there is no other value to send. Instead, 
                        the default attribute's value is the value the server uses if the client 
                        does not send a value.
        """
        self.name = name
        self.display_name = display_name
        self.description = description
        self.type_ = type_
        self.enum = enum
        self.pattern = pattern
        self.min_length = min_length
        self.max_length = max_length
        self.minimum = minimum
        self.maximum = maximum
        self.example = example
        self.repeat = repeat
        self.required = required
        self.default = default

    def to_dict(self):
        return {
            'name': self.name,
            'display_name': self.display_name,
            'description': self.description,
            'type': self.type_,
            'enum': self.enum,
            'pattern': self.pattern,
            'min_length': self.min_length,
            'max_length': self.max_length,
            'minimum': self.minimum,
            'maximum': self.maximum,
            'example': self.example,
            'repeat': self.repeat,
            'required': self.required,
            'default': self.default
        }


class UriParam(Param):
    pass


class QueryParam(Param):
    pass


class FormParam(Param):
    pass


class HeaderParam(Param):
    pass


class Documents(list):

    def append(self, document: Document):
        if not isinstance(document, Document):
            raise TypeError('item is not of type Document')
        super().append(document)

    def to_dict(self):
        return [document.to_dict() for document in self]


class DocumentationRoot:

    def __init__(self, title, version=None, media_type=None,
                 base_uri=None, base_uri_params=None,
                 protocols=None, resources=None, documents=None):
        """
        Documentation root class 
        :param title: The title property is a short plain text description of the RESTful API. 
                      The title property's value SHOULD be suitable for use as a title for 
                      the contained user documentation.
        :param version: API version, The version property is OPTIONAL and should not be used if:
                            - The API itself is not versioned.
                            - The API definition does not change between versions. 
                        The API architect can decide whether a change to user documentation elements, 
                        but no change to the API's resources, constitutes a version change.
        :param media_type: The media types returned by API responses, and expected from API requests 
                           that accept a body, MAY be defaulted by specifying the mediaType property. 
                           This property is specified at the root level of the API definition. 
                           The property's value MAY be a single string with a valid media type:
                           One of the following YAML media types:
                           - text/yaml
                           - text/x-yaml
                           - application/yaml
                           - application/x-yaml*
                           Any type from the list of IANA MIME Media Types, 
                           http://www.iana.org/assignments/media-types
                           A custom type that conforms to the regular expression, 
                           "application/[A-Za-z.-0-1]*+?(json|xml)"
                           For any combination of resource and operation in the API, 
                           if a media type is specified as a key of the body property for 
                           that resource and operation, or if a media type is specified in the mediaType property, 
                           the body MUST be in the specified media types. Moreover, 
                           if the client specifies an Accepts header containing multiple media types 
                           that are allowed by the specification for the requested resource and operation, 
                           the server SHOULD return a body using the media type 
                           in the Accepts header's mediaType list.
        :param base_uri: A RESTful API's resources are defined relative to the API's base URI. 
                         The use of the baseUri field is OPTIONAL to allow describing APIs that 
                         have not yet been implemented. 
                         After the API is implemented (even a mock implementation) and can be accessed 
                         at a service endpoint, the API definition MUST contain a baseUri property. 
                         The baseUri property's value MUST conform to the URI specification [RFC2396] 
                         or a Level 1 Template URI as defined in RFC 6570 [RFC6570].
                         The baseUri property SHOULD only be used as a reference value. 
                         API client generators MAY make the baseUri configurable by the API client's users.
        :param base_uri_params: The parameters (UriParam) used in `base_uri`. 
                                using parameters in base_uri can be like
                                `http://site.com/{my_parameter_name}`.
        :param protocols: A RESTful API can be reached via HTTP, HTTPS, or both. 
                          The protocols property MAY be used to specify the protocols that an API supports. 
                          If the protocols property is not specified, 
                          the protocol specified at the baseUri property is used. 
                          The protocols property MUST be an array of strings, of values "HTTP" and/or "HTTPS".
        :param resources: List of the resources.
        :param documents: List of additional documentations.
        """
        self.title = title
        self.version = version
        self.media_type = media_type
        self.base_uri = base_uri
        self.base_uri_params = [] or base_uri_params
        self.protocols = [] or protocols
        self.documents = Documents()
        self.resources = Resources()

        if documents:
            if isinstance(documents, (tuple, list)):
                self.set_documents(*documents)
            else:
                self.set_documents(documents)

        if resources:
            if isinstance(resources, (tuple, list)):
                self.set_resources(*resources)
            else:
                self.set_resources(resources)

    def set_resources(self, *args):
        for item in args:
            self.resources.append(item)
        return self

    def set_documents(self, *args):
        for item in args:
            self.documents.append(item)
        return self

    def to_dict(self):
        return {
            'title': self.title,
            'version': self.version,
            'base_uri': self.base_uri,
            'media_type': self.media_type,
            'protocols': self.protocols,
            'documents': self.documents.to_dict(),
            'resource': self.resources.to_dict(),
            'base_uri_params': self.base_uri
        }
