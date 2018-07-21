import re
import glob
import textwrap

from .models import Resource

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

    def __init__(self, docstring):
        for line in docstring.split('\n'):
            exploded_line = line.split(' ')
            if line.startswith('@apiDefine '):
                self.name = exploded_line[1]
                self.title = exploded_line[2] if len(exploded_line) > 2 else None
                self.description = ' '.join(exploded_line[3:]) if len(exploded_line) > 3 else None

            elif line.startswith(' '):
                self.description += ' %s' % line.lstrip()

    def __repr__(self):
        return '\n'.join((
            'name: %s' % self.name,
            'title: %s' % self.title,
            'description: %s' % self.description,
        ))


class DocstringApiResource:

    def __init__(self, docstring):
        self.version = None
        self.method = None
        self.path = None
        self.group = None
        self.title = None
        self.params = []
        self.deprecated = False
        self.deprecated_description = None
        self.description = None
        self.error_responses = []
        self.success_responses = []

        docstring = docstring.lstrip()

        prepared_lines = []
        for line in docstring.split('\n'):
            # Join lines
            if line[:1] != '@':
                prepared_lines[-1] = '%s\n%s' % (prepared_lines[-1], line)
            else:
                prepared_lines.append(line)

        for line in prepared_lines:
            if line.startswith('@api '):
                self.parse_api(line)

            elif line.startswith('@apiVersion '):
                self.parse_version(line)

            elif line.startswith('@apiGroup '):
                self.parse_group(line)

            elif line.startswith('@apiDeprecated'):
                self.parse_deprecated(line)

            elif line.startswith('@apiError '):
                self.parse_error(line)

            elif line.startswith('@apiDescription '):
                self.parse_description(line)

            elif line.startswith('@apiParam '):
                self.parse_param(line)

    @staticmethod
    def _get_type(line: str):
        try:
            type_match = next(within_brackets_regex.finditer(line))
            type_ = type_match.group()[1:-1]
        except StopIteration:
            type_match = None
            type_ = None

        return type_match, type_

    @staticmethod
    def _get_group(line: str):
        try:
            group_match = next(within_parentheses_regex.finditer(line))
            group = group_match.group()[1:-1]
        except StopIteration:
            group_match = None
            group = None

        return group_match, group

    @staticmethod
    def _get_name(line: str):
        try:
            name_match = next(single_word_regex.finditer(line))
            name = name_match.group().strip()
        except StopIteration:
            name_match = None
            name = None

        return name_match, name

    @staticmethod
    def _get_path(line: str):
        try:
            path_match = next(path_regex.finditer(line))
            path = path_match.group().strip()
        except StopIteration:
            path_match = None
            path = None

        return path_match, path

    def parse_api(self, line: str):
        type_match, type_ = self._get_type(line)
        if type_match is None:
            raise MissedParameter('Missed api name')

        path_match, path = self._get_path(line)
        if path_match is None:
            raise MissedParameter('Missed path name')

        type_match_span = (-1, -1) if type_match is None else type_match.span()
        path_match_span = path_match.span()

        self.method = type_
        self.path = path
        self.title = line[max(type_match_span[1], path_match_span[1]):].strip()

    def parse_deprecated(self, line: str):
        self.deprecated = True
        self.deprecated_description = line.replace('@apiDeprecated ', '')

    def parse_error(self, line: str):
        # self.error_responses =
        group_match, group = self._get_group(line)
        type_match, type_ = self._get_type(line)
        name_match, name = self._get_name(line)

        group_match_span = (-1, -1) if group_match is None else group_match.span()
        type_match_span = (-1, -1) if type_match is None else type_match.span()
        name_match_span = name_match.span()

        self.error_responses.append({
            'group': group,
            'type': type_,
            'name': name,
            'description': line[max(type_match_span[1], group_match_span[1], name_match_span[1]):].strip()
        })

    def parse_group(self, line: str):
        self.group = line.replace('@apiGroup ', '')

    def parse_version(self, line: str):
        self.version = line.replace('@apiVersion ', '')

    def parse_param(self, line: str):
        group_match, group = self._get_group(line)
        type_match, type_ = self._get_type(line)
        name_match, name = self._get_name(line)

        if name_match is None:
            raise MissedParameter('Missed api parameter `name`')

        if name.startswith('['):
            name = name[1:-1]
            optional = True
        else:
            optional = False

        group_match_span = (-1, -1) if group_match is None else group_match.span()
        type_match_span = (-1, -1) if type_match is None else type_match.span()
        name_match_span = name_match.span()

        self.params.append({
            'name': name,
            'group': group,
            'type': type_,
            'description': line[max(type_match_span[1], group_match_span[1], name_match_span[1]):],
            'optional': optional
        })

    def parse_description(self, line: str):
        self.description = line.replace('@apiDescription ', '')

    def parse_success(self, line: str):
        pass

    def __repr__(self):
        return '\n'.join((
            'method: %s' % self.method,
            'path: %s' % self.path,
            'title: %s' % self.title,
            'version: %s' % self.version,
            'group: %s' % self.group,
            'description %s' % self.description,
            'params: %s' % self.params.__repr__(),
            'error_responses: %s' % self.error_responses.__repr__(),
            'success_responses: %s' % self.success_responses.__repr__()
        ))


class DocstringParser:

    def __init__(self):
        self.resources = []
        self.definitions = []

    def parse_docstring(self, docstring):
        """ Parse docstring """
        docstring = textwrap.dedent(docstring).lstrip()

        if docstring.startswith('@api '):
            self.resources.append(
                DocstringApiResource(docstring)
            )

        elif docstring.startswith('@apiDefine '):
            self.definitions.append(
                DocstringApiDefinition(docstring)
            )

    def prepare_resources(self):
        """ Import definitions into resources """
        for resource in self.resources:
            pass

    def load_from_path(self, base_path: str='.'):
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

        for resource in self.resources:
            print(resource)

        for definition in self.definitions:
            print(definition)

    @staticmethod
    def find_docstring_blocks(source):
        """ Find docstring blocks from python source """
        return re.findall(docstring_block_regex, source)

    def get_resource(self, docstring):
        pass
