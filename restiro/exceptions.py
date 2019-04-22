
class ParserWarning(Warning):
    pass


class DocstringWarning(ParserWarning):
    pass


class InvalidParameter(DocstringWarning):
    pass


class InvalidDefinition(DocstringWarning):
    pass


class MissedParameter(DocstringWarning):
    pass


class DuplicateApiName(DocstringWarning):
    pass
