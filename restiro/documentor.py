from typing import Type

from os.path import join
from importlib import import_module

from restiro import Parser, DocumentationRoot
from restiro.helpers import generate_pot
from restiro.generators import BaseGenerator
from restiro.constants import ansi_orange_fg, ansi_reset


class Documentor:

    def __init__(self, title: str, source_dir: str, base_uri: str=None,
                 generator_type: str='markdown'):
        self.title = title
        self.source_dir = source_dir
        self.base_uri = base_uri
        self.generator_type = generator_type

    def initiate_docs_root(self, locale=None):
        parsed_resources = Parser.load_from_path(self.source_dir)
        docs_root = DocumentationRoot(
            title=self.title,
            base_uri=self.base_uri,
            locale=locale
        )
        docs_root.resources.update(parsed_resources)
        docs_root.load_resource_examples()
        return docs_root

    @property
    def generator(self) -> Type[BaseGenerator]:
        try:
            module_name = (
                'restiro.generators.%s' % self.generator_type
                if self.generator_type in ('json', 'markdown', 'mock') else
                'restiro_%s' % self.generator_type
            )
            mod = import_module(module_name)
            for cname in dir(mod):
                if not cname.endswith('Generator') or cname == 'BaseGenerator':
                    continue

                return getattr(mod, cname)

        except ImportError:
            raise ValueError('Generator not detected %s' % self.generator_type)

    def generate(self, output_dir: str, locales_dir=None, locale=None):
        docs_root = self.initiate_docs_root(locale)
        if locale:
            docs_root.translate_all(locales_dir, locale)

        self.generator(
            docs_root=docs_root,
            destination_dir=output_dir
        ).generate()

        print('=== Build summary ===')
        example_free_resources = []
        for _, resource in docs_root.resources.items():
            print('>>', resource.summary_text[0])

            if len(resource.examples) == 0:
                example_free_resources.append(resource)
                print(f'{ansi_orange_fg}   {resource.summary_text[1]} {ansi_reset}')

            else:
                print(f'   {resource.summary_text[1]}')

            if len(resource.duplicated_parameters) > 0:
                duplicated_params = ', '.join([param.name for param in resource.duplicated_parameters])
                print(f'{ansi_orange_fg}   Duplicated parameter names: {duplicated_params} {ansi_reset}')

        print(docs_root.resources.summary_text[0])
        if len(example_free_resources) > 0:
            print(f'{ansi_orange_fg}{len(example_free_resources)} resources has no example.', ansi_reset)

    def generate_gettext(self, gettext_dir):
        docs_root = self.initiate_docs_root()
        pot_file = join(gettext_dir, 'restiro.pot')
        with open(pot_file, 'w+') as f:
            f.write(generate_pot(docs_root.extract_translations()))
