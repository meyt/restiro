from restiro.helpers import to_snake_case, replace_non_alphabet
from .translation_mixin import TranslationMixin


class Document(TranslationMixin):
    __translation_keys__ = (
        'title',
        'content'
    )

    def __init__(self, title: str, content: str=None):
        """
        Additional documentation.
        The API definition can include a variety of documents that serve 
        as a user guides and reference documentation for the API. 
        Such documents can clarify how the API works or provide business context.
        Documentation-generators MUST include all the sections in an API definition's 
        documentation property in the documentation output, and they MUST preserve the 
        order in which the documentation is declared.

        :param title: The title of documentation.
        :param content: The content of documentation formatted in ``markdown``.
        """
        self.title, self.content = title, content

    @property
    def __filename__(self):
        return replace_non_alphabet(to_snake_case(self.title), '-')

    def to_dict(self):
        return {
            'title': self.title,
            'content': self.content
        }

    @classmethod
    def create_from_dict(cls, data) -> 'Document':
        return cls(
            title=data['title'],
            content=data['content']
        )


class Documents(list):

    def append(self, document: Document):
        if not isinstance(document, Document):
            raise TypeError('item is not of type Document')
        super().append(document)

    def to_dict(self):
        return [document.to_dict() for document in self]

    def extract_translations(self):
        result = []
        for document in self:
            result.extend(document.extract_translations())
        return result

    def translate(self, translator):
        for document in self:
            document.translate(translator)
