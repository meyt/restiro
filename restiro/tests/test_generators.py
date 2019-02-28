import pytest

from os import makedirs
from os.path import join
from shutil import rmtree

from restiro.generators import BaseGenerator, MarkdownGenerator, JSONGenerator
from restiro.tests.helpers import mockup_doc_root, package_dir

temp_dir = join(package_dir, 'temp')


@pytest.fixture('module')
def docs_root():
    return mockup_doc_root()


@pytest.fixture('module', autouse=True)
def wrap_directories():
    rmtree(temp_dir, ignore_errors=True)
    makedirs(temp_dir, exist_ok=True)
    yield True
    rmtree(temp_dir, ignore_errors=True)


def get_destination_dir(provider_name):
    result = join(temp_dir, 'temp', '%s_generator' % provider_name)
    makedirs(result)
    return result


# noinspection PyProtectedMember
def test_base_provider(docs_root):
    provider = BaseGenerator(
        docs_root=docs_root,
        destination_dir=get_destination_dir('base')
    )
    provider._ensure_file('index.txt')
    # already used that file, so returned file_stream is in `append` mode.
    provider._ensure_file('index.txt')


def test_markdown_provider(docs_root):
    provider = MarkdownGenerator(
        docs_root=docs_root,
        destination_dir=get_destination_dir('markdown')
    )
    provider.generate()


def test_json_provider(docs_root):
    provider = JSONGenerator(
        docs_root=docs_root,
        destination_dir=get_destination_dir('json')
    )
    provider.generate()
