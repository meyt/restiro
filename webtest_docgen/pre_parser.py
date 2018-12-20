import re
import glob
import textwrap


docstring_block_regex = re.compile(r'\"\"\"([\s\S]*?)\"\"\"')
within_parentheses_regex = re.compile(r'\(([\s\S]*?)\)')
within_brackets_regex = re.compile(r'{([\s\S]*?)}')
single_word_regex = re.compile(r'\s(\[?\w+\]?)(?=\s?)')
path_regex = re.compile(r'\s\/([\/\w\:]+)(?=\s?)')


class ParserException(Exception):
    pass


class DocstringException(ParserException):
    pass


class InvalidParameter(DocstringException):
    pass


class MissedParameter(DocstringException):
    pass


class DocstringApiDefinition:
    name = None
    title = None
    description = None
    content = ''

    def __init__(self, docstring):
        for line in docstring.split('\n'):
            exploded_line = line.split(' ')
            if line.startswith('@apiDefine '):
                self.name = exploded_line[1]
                self.title = exploded_line[2] \
                    if len(exploded_line) > 2 else None
                self.description = ' '.join(exploded_line[3:]) \
                    if len(exploded_line) > 3 else None

            elif line.startswith(' '):
                self.description += ' %s' % line.lstrip()

            else:
                self.content += line + '\n'

    def to_dict(self):
        return ({
            'name': self.name,
            'title': self.title,
            'description': self.description,
            'content': self.content
        })


class DocstringPreParser:

    def __init__(self):
        self.definitions = []

    def parse_docstring(self, docstring):
        """ Parse docstring """
        docstring = textwrap.dedent(docstring).lstrip()

        if docstring.startswith('@api '):
            pass

        elif docstring.startswith('@apiDefine '):
            self.definitions.append(
                DocstringApiDefinition(docstring).to_dict()
            )

    def load_from_path(self, base_path: str = '.'):
        """ Load python files  """
        for filename in glob.iglob('%s/**/*.py' % base_path, recursive=True):
            self.load_file(filename)
        return self.get_definitions()

    def load_file(self, filename: str):
        """ Open python file and parse docstrings """
        with open(filename, 'r') as f:
            source = f.read()
            docstring_blocks = self.find_docstring_blocks(source)
            for docstring_block in docstring_blocks:
                self.parse_docstring(docstring_block)

    @staticmethod
    def find_docstring_blocks(source):
        """ Find docstring blocks from python source """
        return re.findall(docstring_block_regex, source)

    def get_definitions(self):
        return self.definitions
