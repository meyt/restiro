from .translation_mixin import TranslationMixin

python_type_alias = {
    'int': 'integer',
    'str': 'string',
    'bool': 'boolean',
    'Decimal': 'number',
    'datetime': 'date',
    'date': 'date',
    'float': 'number',
    'TextIOWrapper': 'file',
    'TextIOBase': 'file',
    'BufferedIOBase': 'file',
    'RawIOBase': 'file',
    'IOBase': 'file',
    'IO': 'file',
    'FileIO': 'file',
    'BytesIO': 'file',
    'bytes': 'file',
}


class Param(TranslationMixin):
    __translation_keys__ = (
        'description',
        'display_name'
    )

    def __init__(self, name: str = None, display_name: str = None,
                 description: str = None, type_=None, enum: list = None,
                 pattern: str = None, min_length: int = None,
                 max_length: int = None, minimum: int = None,
                 maximum: int = None, example: str = None, repeat: bool = False,
                 required: bool = False, default: str = None):
        """
        Parameters base class

        :param name: Parameter name
        :param display_name: The ``display_name`` attribute specifies the
                             parameter's display name. It is a friendly name
                             used only for display or documentation purposes.
                             If ``display_name`` is not specified, it defaults
                             to the property's key (the name of
                             the property itself).
        :param description: The description attribute describes the intended
                            use or meaning of the parameter. This value MAY be
                            formatted using Markdown [MARKDOWN].
        :param type_: The ``type_`` attribute specifies the primitive 
                      type of the parameter's resolved value. API clients MUST
                      return/throw an error
                      if the parameter's resolved value does not match the
                      specified type.
                      If type is not specified, it defaults to string.
                      Valid types are:
                      string    Value MUST be a string.
                      number    Value MUST be a number.
                      integer   Value MUST be an integer. 
                                Floating point numbers are not allowed. 
                                The integer type is a subset of the number type.
                      date      Value MUST be a string representation of a date
                                as defined in RFC2616 Section 3.3 [RFC2616].
                                As defined in [RFC2616], all date/time stamps
                                are represented in Greenwich Mean Time (GMT),
                                which for the purposes of HTTP is equal to UTC
                                (Coordinated Universal Time).
                                This is indicated by including "GMT" as the
                                three-letter abbreviation for the timezone.
                                Example: Sun, 06 Nov 1994 08:49:37 GMT.
                      boolean   Value MUST be either the string "true" or
                                "false" (without the quotes).
                      file      (Applicable only to Form properties)
                                Value is a file. Client generators SHOULD use 
                                this type to handle file uploads correctly.
        :param enum: The ``enum`` attribute provides an enumeration of the
                     parameter's valid values.This MUST be an array.
                     If the ``enum`` attribute is defined, API clients and
                     servers MUST verify that a parameter's value matches a
                     value in the enum array.
                     If there is no matching value, the clients and servers
                     MUST treat this as an error.
                     (Applicable only for parameters of type string)
        :param pattern: The ``pattern`` attribute is a regular expression 
                        that a parameter of type string MUST match. Regular
                        expressions MUST follow the regular expression
                        specification from ECMA 262/Perl 5.
                        The pattern MAY be enclosed in double quotes for
                        readability and clarity.
                        (Applicable only for parameters of type string) 
        :param min_length: The ``min_length`` attribute specifies the parameter
                           value's minimum number of characters.
                           (Applicable only for parameters of type string)
        :param max_length: The ``max_length`` attribute specifies the parameter
                           value's maximum number of characters.
                           (Applicable only for parameters of type string)
        :param minimum: The ``minimum`` attribute specifies the parameter's
                        minimum value. (Applicable only for parameters of type
                        number or integer)
        :param maximum: The ``maximum`` attribute specifies the parameter's
                        maximum value. (Applicable only for parameters
                        of type number or integer)
        :param example: The ``example`` attribute shows an example value for
                        the property. This can be used, e.g., by documentation
                        generators to generate sample values for the property.
        :param repeat: The ``repeat`` attribute specifies that the parameter
                       can be repeated. If the parameter can be used multiple
                       times, the repeat parameter value MUST be set to 'true'.
                       Otherwise, the default value is 'false' and the
                       parameter may not be repeated.
        :param required: The ``required`` attribute specifies whether the
                         parameter and its value MUST be present in the API
                         definition. It must be either 'true' if the value MUST
                         be present or 'false' otherwise.
                         In general, parameters are optional unless the
                         required attribute is included and its value set to
                         'true'.
                         For a URI parameter, the required attribute MAY be
                         omitted, but its default value is 'true'.
        :param default: The ``default`` attribute specifies the default value
                        to use for the property if the property is omitted or
                        its value is not specified.
                        This SHOULD NOT be interpreted as a requirement for the
                        client to send the default attribute's value if there
                        is no other value to send. Instead, the default
                        attribute's value is the value the server uses if the
                        client does not send a value.
        """
        self.name = name
        self.display_name = display_name
        self.description = description
        self.type_ = type_ if isinstance(type_, str) else \
            self.get_type_string(type_)
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

    @staticmethod
    def get_type_string(type_):
        if hasattr(type_, '__name__'):
            return python_type_alias.get(type_.__name__, None)

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

    @classmethod
    def create_from_dict(cls, data: dict) -> 'Param':
        kwargs = dict(data)
        kwargs['type_'] = kwargs['type']
        del kwargs['type']
        return cls(**kwargs)


class URLParam(Param):
    def __init__(self, *args, required: bool = True, **kwargs):
        super().__init__(*args, required=required, **kwargs)


class QueryParam(Param):
    pass


class FormParam(Param):
    pass


class HeaderParam(Param):
    pass
