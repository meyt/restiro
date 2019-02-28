
class ParserException(Exception):
    pass


class DocstringException(ParserException):
    pass


class InvalidParameter(DocstringException):
    pass


class InvalidDefinition(DocstringException):
    pass


class MissedParameter(DocstringException):
    pass
