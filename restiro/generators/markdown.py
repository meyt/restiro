from typing import List

from restiro import (
    Resource,
    Document,
    ExampleResponse,
    ExampleRequest,
    ResourceExample
)
from restiro.models.parameters import Param
from restiro.generators import BaseGenerator


class MarkdownRepresentations:

    @staticmethod
    def _repr_response_body(response: ExampleResponse):
        syntax_language = response.body_format
        return '```%s\n%s\n```' % (
            syntax_language.name if syntax_language else '',
            response.body_json or response.body
        )

    @staticmethod
    def _repr_request_headers(request: ExampleRequest):
        return '```\n%s\n```' % (
            request.repr_headers()
        )

    @staticmethod
    def _repr_response_headers(response: ExampleResponse):
        return '```\n%s\n```' % (
            response.repr_headers()
        )

    @staticmethod
    def _repr_request_body(request: ExampleRequest):
        syntax_language = request.body_format
        return '```%s\n%s\n```' % (
            syntax_language.name if syntax_language else '',
            request.body
        )

    @classmethod
    def _repr_example(cls, example: ResourceExample):
        """ Beautify and return example """
        return (
           '#### Request: \n\n'
           '%s\n'  # Headers
           '%s\n'  # Body
           '\n'
           '#### Response: \n\n'
           '%s\n'  # Headers
           '%s\n'  # Body
        ) % (
           cls._repr_request_headers(example.request),
           cls._repr_request_body(example.request),
           cls._repr_response_headers(example.response),
           cls._repr_response_body(example.response),
        )


class MarkdownGenerator(BaseGenerator, MarkdownRepresentations):

    def get_document_filename(self, document: Document):
        return '%s.md' % super().get_document_filename(document)

    def get_resource_filename(self, resource: Resource):
        return '%s.md' % super().get_resource_filename(resource)

    def get_index_filename(self):
        return '%s.md' % super().get_index_filename()

    def write_document(self, f, document: Document):
        f.write('# %s\n\n' % document.title)
        f.write('%s' % document.content)

    # noinspection PyMethodMayBeStatic
    def write_params(self, f, params: List[Param]):
        params_heads = (
            'Name', 'Type', 'Required', 'Default', 'Example', 'enum',
            'Pattern', 'MinLength', 'MaxLength', 'Minimum', 'Maximum',
            'Repeat', 'Description'
        )
        f.write('%s\n' % ' | '.join(params_heads))
        f.write('%s\n' % ' | '.join(list(map(lambda x: '---', params_heads))))
        value_placeholder = ' | '.join(list(map(lambda x: '%s', params_heads)))
        value_placeholder = '%s\n' % value_placeholder
        params.sort(key=lambda x: x.name)
        for param in params:
            f.write(
                value_placeholder % (
                    param.name,
                    param.type_,
                    '`True`' if param.required else '`False`',
                    param.default or '',
                    param.example or '',
                    param.enum or '',
                    param.pattern or '',
                    param.min_length or '',
                    param.max_length or '',
                    param.minimum or '',
                    param.maximum or '',
                    '`True`' if param.repeat else '`False`',
                    (param.description or '').replace('\n', ' ')
                )
            )

    # noinspection PyMethodMayBeStatic
    def write_resource_parameters(self, f, resource: Resource):

        if len(resource.uri_params) > 0:
            f.write('### URI parameters\n\n')
            self.write_params(f, resource.uri_params)
            f.write('\n')

        if len(resource.query_params) > 0:
            f.write('### Query-string parameters\n\n')
            self.write_params(f, resource.query_params)
            f.write('\n')

        if len(resource.header_params) > 0:
            f.write('### Header parameters\n\n')
            self.write_params(f, resource.header_params)
            f.write('\n')

        if len(resource.form_params) > 0:
            f.write('### Form parameters\n\n')
            self.write_params(f, resource.form_params)
            f.write('\n')

    def write_resource(self, f, resource: Resource):
        f.write('# %s\n\n' % (resource.display_name or 'untitled'))
        f.write('## `%s` `%s`\n\n' % (str(resource.method).upper(),
                                      resource.path))

        if resource.description:
            f.write('%s\n\n' % resource.description)

        if len(resource.params) > 0:
            f.write('\n## Parameters\n\n')
            self.write_resource_parameters(f, resource)

        if len(resource.examples) > 0:
            f.write('## Examples\n\n')
            for index, example in enumerate(resource.examples):
                f.write('### #%s\n\n' % index)
                f.write(self._repr_example(example))
                f.write('\n---\n')

    def write_index(self, file_stream):
        file_stream.write(
            '# %s\n\n' % self.docs_root.title or 'untitled'
        )

        if len(self.docs_root.documents) > 0:
            file_stream.write('\n## Documents\n\n')
            for document in self.docs_root.documents:
                file_stream.write('- %s\n' % document.title)

        if len(self.docs_root.resources) > 0:
            file_stream.write('\n## Resources\n\n')
            for resource_key, resource in self.docs_root.resources.items():
                file_stream.write(
                    '- `%s` `%s` \n' % (resource.path, resource.method)
                )
