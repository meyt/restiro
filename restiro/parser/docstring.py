
import re
import glob
import textwrap

from restiro.models import Resources
from restiro.constants import docstring_block_regex
from restiro.parser.resource import DocstringApiResource
from restiro.parser.definition import DocstringApiDefinition


class DocstringParser:

    def parse_docstring(self, docstring, filename, start_line):
        raise NotImplementedError

    def load_from_path(self, base_path: str = '.'):
        """ Load python files  """
        for filename in glob.iglob('%s/**/*.py' % base_path, recursive=True):
            self.load_file(filename)

    def load_file(self, filename: str):
        """ Open python file and parse docstrings """
        with open(filename, 'r') as f:
            source = f.read()
            docstring_blocks = self.find_docstring_blocks(source)
            for docstring_block in docstring_blocks:
                self.parse_docstring(docstring_block[0], filename,
                                     docstring_block[1])

    @staticmethod
    def find_docstring_blocks(source):
        """ Find docstring blocks from python source
            and return them with line number"""

        re_newline = re.compile(r'\n')
        all_doc_blocks = []
        for line in re.finditer(docstring_block_regex, source):
            start_line = len(re_newline.findall(source, 0, line.start())) + 1
            all_doc_blocks.append((
                textwrap.dedent(line.group()[3:-3]).lstrip(),
                start_line))

        return all_doc_blocks


class DocstringResourceParser(DocstringParser):

    def __init__(self, definitions: dict):
        self.resources = []
        self.definitions = definitions

    def parse_docstring(self, docstring, filename, start_line):
        if docstring.startswith('@api '):
            self.resources.append(
                DocstringApiResource(docstring,
                                     filename=filename,
                                     start_line=start_line,
                                     definitions=self.definitions)
            )

    def export_to_model(self) -> Resources:
        result = Resources()
        for resource in self.resources:
            result.append(resource.to_model())
        return result


class DocstringDefinitionParser(DocstringParser):

    def __init__(self):
        self.definitions = {}

    def parse_docstring(self, docstring, filename, start_line):
        if docstring.startswith('@apiDefine '):
            definition = DocstringApiDefinition(docstring)
            self.definitions[definition.name] = definition
