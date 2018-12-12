from webtest_docgen.parser import DocstringParser
from os.path import dirname


# test description
doc = DocstringParser()
doc.load_file('webtest_docgen/tests/stuff/test_project/test_description.py')
