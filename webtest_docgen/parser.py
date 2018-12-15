import re
import glob
import textwrap
from webtest_docgen.pre_parser import DocstringPreParser
from .models import (
    Resource,
    Response,
    FormParam,
    ResourceExample,
    Request,
    Resources)

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


class InvalidDefinition(DocstringException):
    pass


class MissedParameter(DocstringException):
    pass


class DocstringApiResource:

    def __init__(self, docstring, definition: list = None):
        self.version = None
        self.method = None
        self.path = None
        self.group = None
        self.title = None
        self.params = []
        self.deprecated = False
        self.definition = definition
        self.deprecated_description = None
        self.description = None
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
                self.title = self.title.strip()

            elif line.startswith('@apiVersion '):
                self.parse_version(line)
                self.version = self.version.strip()

            elif line.startswith('@apiGroup '):
                self.parse_group(line)
                self.group = self.group.strip()

            elif line.startswith('@apiDeprecated'):
                self.parse_deprecated(line)

            # elif line.startswith('@apiError '):
                # self.parse_error(line)
                # pass
            elif line.startswith('@apiDescription '):
                self.parse_description(line)
                self.description = self.description.strip()

            elif line.startswith('@apiParam '):
                self.parse_param(line)

            elif line.startswith('@apiSuccess '):
                self.parse_success(line)

            elif line.startswith('@apiUse '):
                new_lines = self.parse_use_define(line)
                prepared_lines.extend(new_lines)

    def parse_use_define(self, line: str):
        name_match, name = self._get_name(line)
        name = name.strip()
        definition_lines = []
        is_found = None
        for define in self.definition:
            if define['name'] == name:
                definition_lines = str(define['content']).split('\n')
                is_found = True
        if not is_found:
            raise InvalidDefinition('There is not such apiDefine %s' % name)

        return definition_lines

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

    # def parse_error(self, line: str):
    #     # self.error_responses =
    #     group_match, group = self._get_group(line)
    #     type_match, type_ = self._get_type(line)
    #     name_match, name = self._get_name(line)
    #
    #     group_match_span = (-1, -1) \
    #         if group_match is None else group_match.span()
    #     type_match_span = (-1, -1) if type_match is None
    #                                else type_match.span()
    #     name_match_span = name_match.span()

        # self.error_responses.append({
        #     'group': group,
        #     'type': type_,
        #     'name': name,
        #     'description': line[max(type_match_span[1], group_match_span[1],
        #                             name_match_span[1]):].strip()
        # })

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

        group_match_span = (-1, -1) \
            if group_match is None else group_match.span()
        type_match_span = (-1, -1) if type_match is None else type_match.span()
        name_match_span = name_match.span()
        description = line[max(type_match_span[1],
                               group_match_span[1], name_match_span[1]):]
        des_lines = description.split('\n')
        des_result = ''
        for st in des_lines:
            des_result = ' '.join((des_result, st.strip())) \
                if len(des_lines) > 1 else st.strip()

        names = name.split('=')
        default = names[1] if len(names) > 1 else None

        new_param = FormParam(name=names[0], description=des_result,
                              type_=type_, required=optional, default=default)
        self.params.append(new_param)

    def parse_description(self, line: str):
        temp_description = line.replace('@apiDescription ', '')
        # reg = re.compile('\n(?!\s*\n)([\r\t\f\v])*')
        des = temp_description.split('\n')
        t = ''
        for s in des:
            if s not in ('', ' ', '\t', '\n'):
                t = t + s.strip() + ' '
            else:
                t = t + '\n'
        self.description = t if not self.description \
            else '\n'.join((self.description, t))

    def parse_success(self, line: str):
        group_match, group = self._get_group(line)
        type_match, type_ = self._get_type(line)
        name_match, name = self._get_name(line)

        if name_match is None:
            raise MissedParameter('Missed api parameter `name`')

        group_match_span = (-1, -1) \
            if group_match is None else group_match.span()
        type_match_span = (-1, -1) if type_match is None else type_match.span()
        name_match_span = name_match.span()
        description = line[max(type_match_span[1],
                               group_match_span[1], name_match_span[1]):]
        des_lines = description.split('\n')
        des_result = ''
        for st in des_lines:
            des_result = des_result + st.strip() + ' '

        response = '\n'.join((
            'name: %s' % name,
            'group: %s' % group,
            'type: %s' % type_,
            'description: %s' % des_result
        ))

        new_response = Response(
            status=200, headers={},
            body=response)
        request = Request(path=self.path, method=self.method, text='')
        example = ResourceExample(request, new_response)

        self.success_responses.append(example)

    def __repr__(self):
        return '\n'.join((
            'method: %s' % self.method,
            'path: %s' % self.path,
            'title: %s' % self.title,
            'version: %s' % self.version,
            'group: %s' % self.group,
            'description: %s' % self.description,
            'params: %s' % self.params.__repr__(),
            # 'error_responses: %s' % self.error_responses.__repr__(),
            'success_responses: %s' % self.success_responses.__repr__()
        ))

    def to_dict(self):
        return ({
            'method': self.method,
            'path': self.path,
            'title': self.title,
            'version': self.version,
            'group': self.group,
            'description': self.description,
            'params': self.params,
            'success_responses': self.success_responses
        })

    def to_model(self):
        resource = Resource(path=self.path,
                            method=self.method,
                            tags=[self.group],
                            display_name=self.title,
                            description=self.description,
                            params=self.params,
                            examples=self.success_responses
                            )
        return resource


class DocstringParser:

    def __init__(self):
        self.resources = []
        self.definitions = []

    def parse_docstring(self, docstring):
        """ Parse docstring """
        docstring = textwrap.dedent(docstring).lstrip()

        if docstring.startswith('@api '):
            self.resources.append(
                DocstringApiResource(docstring, self.definitions)
            )

        elif docstring.startswith('@apiDefine '):
            pass

    def load_from_path(self, base_path: str = '.'):
        pre = DocstringPreParser()
        self.definitions.extend(pre.load_from_path(base_path))

        """ Load python files  """
        for filename in glob.iglob('%s/**/*.py' % base_path, recursive=True):
            self.load_file(filename)

        # for resource in self.resources:
        #     print(resource)

        return self.resources

    def load_file(self, filename: str):
        """ Open python file and parse docstrings """
        with open(filename, 'r') as f:
            source = f.read()
            docstring_blocks = self.find_docstring_blocks(source)
            for docstring_block in docstring_blocks:
                self.parse_docstring(docstring_block)

        return self.resources

    @staticmethod
    def find_docstring_blocks(source):
        """ Find docstring blocks from python source """
        return re.findall(docstring_block_regex, source)

    def export_to_model(self):
        result = dict()
        for resource in self.resources:
            if resource.version not in result.keys():
                result[resource.version] = Resources()
            result[resource.version].append(resource.to_model())

        return result
