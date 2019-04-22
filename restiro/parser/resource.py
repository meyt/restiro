from warnings import warn_explicit
from restiro.constants import (
    within_brackets_regex,
    within_parentheses_regex,
    single_word_regex,
    path_regex
)

from restiro.models import (
    FormParam, QueryParam, HeaderParam, URLParam, Resource
)

from restiro.exceptions import (
    MissedParameter,
    InvalidDefinition,
    DuplicateApiName
)
from restiro.helpers import sanitize_multi_line

params_map = {
    'form': FormParam,
    'query': QueryParam,
    'head': HeaderParam,
    'url': URLParam
}


class DocstringApiResource:

    def __init__(self, docstring, filename, start_line,
                 definitions: dict = None):
        self.version = None
        self.method = None
        self.path = None
        self.group = None
        self.title = None
        self.params = []
        self.permissions = []
        self.definitions = definitions
        self.description = None
        self.filename = filename
        self.start_line = start_line + 1

        prepared_lines = []
        for index, line in enumerate(docstring.split('\n')):
            # Join lines
            if line[:1] != '@':
                prepared_lines[-1][0] = '%s \n%s' % \
                                        (prepared_lines[-1][0], line)
            else:
                prepared_lines.append([line, index])

        for line in prepared_lines:
            if line[0].startswith('@api '):
                if self.parse_api(line[0], line[1]+self.start_line):
                    self.title = self.title.strip()

            elif line[0].startswith('@apiVersion '):
                self.parse_version(line[0])
                self.version = self.version.strip()

            elif line[0].startswith('@apiGroup '):
                self.parse_group(line[0])
                self.group = self.group.strip()

            elif line[0].startswith('@apiPermission '):
                self.parse_permission(line[0])

            elif line[0].startswith('@apiDescription '):
                self.parse_description(line[0], line[1]+self.start_line)

            elif line[0].startswith('@apiParam '):
                self.parse_param(line[0], line[1]+self.start_line, 'form')

            elif line[0].startswith('@apiQueryParam '):
                self.parse_param(line[0], line[1]+self.start_line, 'query')

            elif line[0].startswith('@apiUrlParam '):
                self.parse_param(line[0], line[1]+self.start_line, 'url')

            elif line[0].startswith('@apiHeadParam '):
                self.parse_param(line[0], line[1]+self.start_line, 'head')

            elif line[0].startswith('@apiUse '):
                new_lines = self.parse_use_define(
                    line[0], line[1]+self.start_line)
                for lines in new_lines:
                    prepared_lines.append([lines, line[1]])

    def parse_use_define(self, line: str, index):
        name_match, name = self._get_name(line)
        name = name.strip()
        definition_lines = []
        is_found = None
        for key, define in self.definitions.items():
            if key == name:
                definition_lines = str(define.content).split('\n')
                is_found = True
        if not is_found:
            warn_explicit('There is not such apiDefine %s' % name,
                          InvalidDefinition, self.filename, index)

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

    def parse_api(self, line: str, index: int):
        type_match, type_ = self._get_type(line)
        if type_match is None:
            warn_explicit('Missed api name',
                          MissedParameter, self.filename, index)

        path_match, path = self._get_path(line)
        if path_match is None:
            warn_explicit('Missed path name',
                          MissedParameter, self.filename, index)
            return False

        type_match_span = (-1, -1) if type_match is None else type_match.span()
        path_match_span = path_match.span()

        self.method = type_
        self.path = path
        self.title = line[max(type_match_span[1], path_match_span[1]):].strip()
        return True

    def parse_permission(self, line: str):
        permissions = line.replace('@apiPermission ', '')
        permissions = permissions.split(',')
        for permission in permissions:
            self.permissions.append(permission.strip())

    def parse_group(self, line: str):
        self.group = line.replace('@apiGroup ', '')

    def parse_version(self, line: str):
        self.version = line.replace('@apiVersion ', '')

    def parse_param(self, line: str, index: int, param_type: str):
        group_match, group = self._get_group(line)
        type_match, type_ = self._get_type(line)
        name_match, name = self._get_name(line)

        if name_match is None:
            warn_explicit('Missed api parameter `name`', MissedParameter,
                          self.filename, index)
            return False

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
            if len(des_lines) > 1:
                des_result = ' '.join((des_result, st.strip()))
            else:
                st.strip()

        names = name.split('=')
        default = names[1] if len(names) > 1 else None

        self.params.append({
            'name': name,
            'group': group,
            'type': type_,
            'default': default,
            'description': line[max(type_match_span[1], group_match_span[1],
                                    name_match_span[1]):],
            'optional': optional,
            'param_type': param_type
        })
        return True

    def parse_description(self, line: str, index: int):
        temp_description = line.replace('@apiDescription ', '')
        if self.description:
            warn_explicit('There is already one description', DuplicateApiName,
                          self.filename, index)
        self.description = sanitize_multi_line(temp_description)

    def __repr__(self):
        return '\n'.join((
            'method: %s' % self.method,
            'path: %s' % self.path,
            'title: %s' % self.title,
            'version: %s' % self.version,
            'group: %s' % self.group,
            'description: %s' % self.description,
            'permissions: %s' % self.permissions.__repr__(),
            'params: %s' % self.params.__repr__()
        ))

    def to_model(self):

        params_in_model = list(map(
            lambda param: params_map[param['param_type']](
                name=param['name'],
                description=param['description'],
                type_=param['type'],
                required=not param['optional'],
                default=param['default']
            ),
            self.params
        ))

        return Resource(
            path=self.path,
            method=self.method,
            tags=[self.group],
            display_name=self.title,
            description=self.description,
            security={'roles': self.permissions},
            params=params_in_model
        )
