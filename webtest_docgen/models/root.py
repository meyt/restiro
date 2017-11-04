from typing import List, Union
from .resource import Resource, Resources
from .document import Document, Documents
from .parameters import UriParam


class DocumentationRoot:

    def __init__(self, title: str, version: str=None, media_type: str=None,
                 base_uri: str=None, base_uri_params: List[UriParam]=None,
                 protocols: List[str]=None, resources: Union[Resource, List[Resource]]=None,
                 documents: Union[Document, List[Document]]=None):
        """
        Documentation root class 
        :param title: The ``title`` property is a short plain text description of the RESTful API. 
                      The ``title`` property's value SHOULD be suitable for use as a title for 
                      the contained user documentation.
        :param version: API version, The ``version`` property is OPTIONAL and should not be used if:
                            - The API itself is not versioned.
                            - The API definition does not change between versions. 
                        The API architect can decide whether a change to user documentation elements, 
                        but no change to the API's resources, constitutes a version change.
        :param media_type: The media types returned by API responses, and expected from API requests 
                           that accept a body, MAY be defaulted by specifying the ``media_type`` property. 
                           This property is specified at the root level of the 
                           API definition :class:`DocumentationRoot`. 
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
                           that resource and operation, or if a media type is specified in the 
                           ``media_type`` property, the body MUST be in the specified media types. 
                           Moreover, if the client specifies an Accepts header containing multiple 
                           media types that are allowed by the specification for the requested 
                           resource and operation, the server SHOULD return a body using 
                           the media type in the Accepts header's mediaType list.
        :param base_uri: A RESTful API's resources are defined relative to the API's base URI. 
                         The use of the ``base_uri`` field is OPTIONAL to allow describing APIs that 
                         have not yet been implemented. 
                         After the API is implemented (even a mock implementation) and can be accessed 
                         at a service endpoint, the API definition MUST contain a ``base_uri`` property. 
                         The ``base_uri`` property's value MUST conform to the URI specification [RFC2396] 
                         or a Level 1 Template URI as defined in RFC 6570 [RFC6570].
                         The ``base_uri`` property SHOULD only be used as a reference value. 
                         API client generators MAY make the ``base_uri`` configurable by the API client's users.
        :param base_uri_params: The parameters (`UriParam`) used in ``base_uri``. 
                                using parameters in ``base_uri`` can be like
                                ``http://site.com/{my_parameter_name}``.
        :param protocols: A RESTful API can be reached via HTTP, HTTPS, or both. 
                          The ``protocols`` property MAY be used to specify the protocols that an API supports. 
                          If the ``protocols`` property is not specified, 
                          the protocol specified at the ``base_uri`` property is used. 
                          The ``protocols`` property MUST be an array of strings, of values "HTTP" and/or "HTTPS".
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
            if isinstance(documents, list):
                self.set_documents(*documents)
            else:
                self.set_documents(documents)

        if resources:
            if isinstance(resources, list):
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
