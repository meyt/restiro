
import re
import glob
import textwrap

from restiro.models import Resources
from restiro.constants import docstring_block_regex
from restiro.parser.resource import DocstringApiResource
from restiro.parser.definition import DocstringApiDefinition


class DocstringParser:

    def parse_docstring(self, docstring):
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
                self.parse_docstring(docstring_block)

    @staticmethod
    def find_docstring_blocks(source):
        """ Find docstring blocks from python source """
        return re.findall(docstring_block_regex, source)


class DocstringResourceParser(DocstringParser):

    def __init__(self, definitions: dict):
        self.resources = []
        self.definitions = definitions

    def parse_docstring(self, docstring):
        docstring = textwrap.dedent(docstring).lstrip()

        if docstring.startswith('@api '):
            self.resources.append(
                DocstringApiResource(docstring, self.definitions)
            )

    def export_to_model(self) -> Resources:
        result = Resources()
        for resource in self.resources:
            result.append(resource.to_model())
        return result


class DocstringDefinitionParser(DocstringParser):

    def __init__(self):
        self.definitions = {}

    def parse_docstring(self, docstring):
        docstring = textwrap.dedent(docstring).lstrip()
        if docstring.startswith('@apiDefine '):
            definition = DocstringApiDefinition(docstring)
            self.definitions[definition.name] = definition
