from restiro import Parser, DocumentationRoot
from restiro.generators import MarkdownGenerator, JSONGenerator


class Documentor:

    def __init__(self, title: str, source_dir: str, output_dir: str,
                 base_uri: str=None, generator_type: str='markdown'):
        parsed_resources = Parser.load_from_path(source_dir)

        self.docs_root = DocumentationRoot(
            title=title,
            base_uri=base_uri
        )
        self.docs_root.resources.update(parsed_resources)
        self.docs_root.load_resource_examples()

        if generator_type == 'markdown':
            self.generator = MarkdownGenerator(docs_root=self.docs_root,
                                               destination_dir=output_dir)

        elif generator_type == 'json':
            self.generator = JSONGenerator(docs_root=self.docs_root,
                                           destination_dir=output_dir)

        else:
            raise ValueError('Invalid documentation generator type (%s)' %
                             generator_type)

    def generate(self):
        self.generator.generate()
