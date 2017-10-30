from . import BaseProvider


class MarkdownProvider(BaseProvider):

    def get_resource_filename(self, resource):
        return '%s.md' % super().get_resource_filename(resource)

    def get_index_filename(self):
        return '%s.md' % super().get_index_filename()

    @staticmethod
    def _repr_example(example):
        """ Beautify and return example """
        syntax_language = example.response.body_format
        return '```%s\n%s\n```\n```\n%s\n```' % (
            ' %s' % syntax_language.name if syntax_language else '',
            example.request.__repr__(),
            example.response.__repr__()
        )

    def write_resource(self, f, resource):
        f.write('# %s\n\n' % (resource.display_name or 'untitled'))
        f.write('## `%s` `%s`\n\n' % (str(resource.method).upper(), resource.path))

        if resource.description:
            f.write('%s\n\n' % resource.description)

        if len(resource.examples) > 0:
            f.write('## Examples\n\n')
            for example in resource.examples:
                f.write(self._repr_example(example))
                f.write('\n---\n')

    def write_index(self, file_stream):
        file_stream.write('# %s `%s`\n\n' % (self.docs_root.title or 'untitled', self.docs_root.version))
        if len(self.docs_root.documents) > 0:
            file_stream.write('\n## Documents\n\n')
            for document in self.docs_root.documents:
                file_stream.write('- %s\n' % document.title)

        if len(self.docs_root.resources) > 0:
            file_stream.write('\n## Resources\n\n')
            for resource_key, resource in self.docs_root.resources.items():
                file_stream.write('- `%s` `%s` \n' % (resource.path, resource.method))
