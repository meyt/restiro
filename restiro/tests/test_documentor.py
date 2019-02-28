from os import makedirs
from os.path import join

from restiro import Documentor
from restiro.tests.helpers import stuff_dir, package_dir

temp_dir = join(package_dir, 'temp')


def get_destination_dir(provider_name):
    result = join(temp_dir, 'temp', '%s_generator' % provider_name)
    makedirs(result)
    return result


def test_documentor():
    online_store_dir = join(stuff_dir, 'online_store')

    documentor = Documentor(
        title='Online Store',
        source_dir=online_store_dir,
        output_dir=get_destination_dir('markdown'),
        generator_type='markdown'
    )

    documentor.generate()
