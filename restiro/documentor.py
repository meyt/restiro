from typing import Type

from os.path import join
from importlib import import_module

from restiro import Parser, DocumentationRoot
from restiro.helpers import generate_pot
from restiro.generators import BaseGenerator


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

    def generate_gettext(self, gettext_dir):
        docs_root = self.initiate_docs_root()
        pot_file = join(gettext_dir, 'restiro.pot')
        with open(pot_file, 'w+') as f:
            f.write(generate_pot(docs_root.extract_translations()))
