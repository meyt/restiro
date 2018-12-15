import unittest
from webtest_docgen.parser import DocstringParser
from webtest_docgen.parser import DocstringApiResource
from webtest_docgen.models import Resource, FormParam


class ParserTestCase(unittest.TestCase):

    def test_parser(self):
        parser = DocstringParser()

        resources = [
            Resource(
                path='/media',
                method='post',
                description='',
                tags=['Media'],
                display_name='Upload a media file',
                params=[
                    FormParam(
                        name='file',
                        type_='File',
                        required=False
                    ),
                    FormParam(
                        name='visible',
                        type_='Boolean',
                        required=True
                    ),
                    FormParam(
                        name='something',
                        type_='String',
                        required=True
                    )
                ],
                examples=[]
            )
        ]

        # test parser
        result = parser.load_file('webtest_docgen/tests/stuff/'
                                  'test_project/test_doc.py')

        self.assertIsInstance(result[0], DocstringApiResource)
        self.assertEqual(result[0].method, resources[0].method)
        self.assertEqual(result[0].path, resources[0].path)
        self.assertEqual(result[0].title, resources[0].display_name)
        self.assertEqual(result[0].group, resources[0].tags[0])
        self.assertEqual(len(result[0].params),
                         len(resources[0].form_params))
        self.assertEqual(result[0].params[0].name,
                         resources[0].form_params[0].name)
        self.assertEqual(result[0].params[0].type_,
                         resources[0].form_params[0].type_)
        self.assertEqual(result[0].params[0].required,
                         resources[0].form_params[0].required)

        # test to_dict and represent of a resource
        result_dict = result[0].to_dict()
        self.assertEqual(result_dict['success_responses'], [])
        result_rep = result[0].__repr__()
        self.assertIsInstance(result_rep, str)

        # test multi line description
        result = parser.load_file('webtest_docgen/tests/stuff/test_project/'
                                  'multiline_description.py')

        self.assertEqual(result[1].description, 'this is a description '
                                                'for test this api \nand some'
                                                ' other \nthis is 1')

        # test multi descriptions
        result = parser.load_file('webtest_docgen/tests/stuff/test_project/'
                                  'multi_description.py')

        doc = DocstringParser()
        # no name api
        with self.assertRaises(Exception):
            doc.load_file('webtest_docgen/tests/stuff/wrong_usecases/'
                          'api_name.py')
        # api without path
        with self.assertRaises(Exception):
            doc.load_file('webtest_docgen/tests/stuff/wrong_usecases/'
                          'api_path.py')

        # no name parameter
        with self.assertRaises(Exception):
            doc.load_file('webtest_docgen/tests/stuff/wrong_usecases/'
                          'missed_parameter.py')

        with self.assertRaises(Exception):
            doc.load_file('webtest_docgen/tests/stuff/wrong_usecases/'
                          'success_parameter.py')

        # test apiDefine and apiUse
        parser.load_from_path('webtest_docgen/tests/stuff/test_project')
        self.assertEqual(len(parser.definitions[0].keys()), 4)

        # use of not define block
        with self.assertRaises(Exception):
            doc.load_file('webtest_docgen/tests/stuff/'
                          'wrong_usecases/wrong_use.py')

        result = parser.export_to_model()
        self.assertEqual(len(result), 1)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
