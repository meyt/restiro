import warnings
from os.path import join

from restiro import (
    Parser,
    Resource,
    QueryParam,
    URLParam
)
from restiro.parser.docstring import (
    DocstringResourceParser,
    DocstringDefinitionParser
)
from restiro.tests.helpers import stuff_dir
from restiro.exceptions import (
    MissedParameter,
    InvalidDefinition,
    DuplicateApiName
)


def test_parser(recwarn):
    online_store_path = join(stuff_dir, 'online_store')
    wrong_usecases_path = join(stuff_dir, 'wrong_usecases')

    resources = Parser.load_from_path(online_store_path)

    example_resource = [
        Resource(
            path='/product',
            method='get',
            display_name='Get all products',
            tags=['Product'],
            params=[
                QueryParam(
                    name='sort',
                    type_=None,
                    required=False
                )
            ],
            security={'roles': ['god', 'operator']}
        ),
        Resource(
            path='/product/:productId',
            method='get',
            display_name='Get a seller',
            params=[
                URLParam(
                    name='productId',
                    required=True,
                    type_='Integer')
            ]
        )
    ]

    # Key of resource in Resources 'path-method'
    resource = resources['/product-get']

    assert resource.method == example_resource[0].method
    assert resource.path == example_resource[0].path
    assert resource.display_name == example_resource[0].display_name
    assert resource.tags[0] == example_resource[0].tags[0]
    assert resource.security == example_resource[0].security
    assert len(resource.params) == 4
    assert isinstance(resource.params[0], QueryParam)
    assert resource.params[0].name == example_resource[0].params[0].name
    assert resource.params[0].type_ == example_resource[0].params[0].type_
    assert (
        resource.params[0].required == example_resource[0].params[0].required
    )

    # test represent of a resource
    result_rep = resource.__repr__()
    assert isinstance(result_rep, str)

    definition_parser = DocstringDefinitionParser()
    definition_parser.load_from_path(online_store_path)
    doc_parser = DocstringResourceParser(definition_parser.definitions)

    # An api without name
    warnings.simplefilter("always")
    doc_parser.load_file(join(wrong_usecases_path, 'wrong_api_name.py'))
    assert len(recwarn) == 1
    some_warning = recwarn.pop(MissedParameter)
    assert some_warning is not None
    assert some_warning.lineno == 7

    # api without path
    doc_parser.load_file(join(wrong_usecases_path, 'wrong_api_path.py'))
    assert len(recwarn) == 1
    some_warning = recwarn.pop(MissedParameter)
    assert some_warning is not None
    assert some_warning.lineno == 7

    # no name parameter
    doc_parser.load_file(
        join(wrong_usecases_path, 'missed_parameter_name.py'))
    assert len(recwarn) == 1
    some_warning = recwarn.pop(MissedParameter)
    assert some_warning is not None
    assert some_warning.lineno == 14

    # use of not define block
    doc_parser.load_file(join(wrong_usecases_path, 'wrong_api_use.py'))
    assert len(recwarn) == 1
    some_warning = recwarn.pop(InvalidDefinition)
    assert some_warning is not None
    assert some_warning.lineno == 16

    # api without path
    doc_parser.load_file(join(wrong_usecases_path, 'duplicate_description.py'))
    assert len(recwarn) == 1
    some_warning = recwarn.pop(DuplicateApiName)
    assert some_warning is not None
    assert some_warning.lineno == 15

