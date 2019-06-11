import argparse
from importlib.util import find_spec

from os import scandir, makedirs
from os.path import dirname, isdir, basename, join, realpath

from restiro import Documentor
from restiro.helpers import validate_locale_name


def main():
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
        '-g', '--generator',
        choices=('markdown', 'json', 'spa_material', 'mock'),
        default='markdown', help='Generator, default: markdown')
    parser.add_argument(
        '-l', '--locales', default='./locales', help='Locales directory')
    parser.add_argument(
        '--build-gettext', default=False, const=True, nargs='?',
        help='Build .POT templates')

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


def mock():
    import json
    from restiro.mock_server import MockServer, DocumentationRoot
    from wsgiref.simple_server import make_server
    parser = argparse.ArgumentParser(description='Restiro Mock Server')
    parser.add_argument('--root', default='./index.json')
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--port', type=int, default=3010)
    args = parser.parse_args()

    root_file = args.root or realpath

    with open(root_file, 'r') as f:
        root_data = json.load(f)

    docs_root = DocumentationRoot.create_from_dict(root_data)
    httpd = make_server(
        app=MockServer(docs_root),
        host=args.host,
        port=args.port
    )
    print(
        'Mock server is now running on https://%s:%s ...' %
        (args.host, args.port)
    )
    httpd.serve_forever()
