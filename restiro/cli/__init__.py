import argparse
from importlib.util import find_spec

from os import scandir, makedirs
from os.path import dirname, isdir, basename, join

from restiro import Documentor
from restiro.helpers import validate_locale_name

parser = argparse.ArgumentParser(description='Restiro Builder')
parser.add_argument(
    'src', help='Project module name')
parser.add_argument(
    '-t', '--title', help='Project title')
parser.add_argument(
    '-o', '--output', default='./docs', help='Output directory')
parser.add_argument(
    '-b', '--base-uri', help='Base URI')
parser.add_argument(
    '-g', '--generator', choices=('markdown', 'json', 'spa_material'),
    default='markdown', help='Generator, default: markdown')
parser.add_argument(
    '-l', '--locales', default='./locales', help='Locales directory')
parser.add_argument(
    '--build-gettext', default=False, const=True, nargs='?',
    help='Build .POT templates')


def main():
    args = parser.parse_args()
    title = args.title or args.src
    source_dir = dirname(find_spec(args.src).origin)
    locales_dir = args.locales
    output_base_dir = args.output

    def get_documentor():
        return Documentor(
            title=title,
            base_uri=args.base_uri,
            source_dir=source_dir,
            generator_type=args.generator
        )

    if args.build_gettext:
        gettext_dir = join(locales_dir, 'gettext')
        makedirs(gettext_dir, exist_ok=True)

        get_documentor().generate_gettext(gettext_dir)
        print('gettext .POT templates generated in: %s' % gettext_dir)
        return

    if isdir(locales_dir):
        for entry in scandir(locales_dir):
            if not entry.is_dir():
                continue

            locale = basename(entry.path)

            if not validate_locale_name(locale):
                continue

            output_dir = join(output_base_dir, locale)
            makedirs(output_dir, exist_ok=True)
            get_documentor().generate(output_dir, locales_dir, locale)

            print('Documentation build success. (%s)' % output_dir)

    else:
        get_documentor().generate(output_base_dir)
        print('Documentation build success. (%s)' % output_base_dir)
