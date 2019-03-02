import argparse
from importlib.util import find_spec

from os.path import dirname
from restiro import Documentor

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
    '-g', '--generator', choices=('markdown', 'json'),
    default='markdown', help='Generator, default: markdown')


def main():
    args = parser.parse_args()
    title = args.title or args.src
    source_dir = dirname(find_spec(args.src).origin)

    documentor = Documentor(
        title=title,
        base_uri=args.base_uri,
        source_dir=source_dir,
        output_dir=args.output,
        generator_type=args.generator
    )

    documentor.generate()
