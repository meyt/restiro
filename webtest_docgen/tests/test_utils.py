import unittest
from webtest_docgen.utils import to_snake_case, replace_non_alphabet, CaseInsensitiveDict


class UtilsTestCase(unittest.TestCase):

    def test_to_snake_case(self):
        self.assertEqual(to_snake_case('snakesOnAPlane'), 'snakes_on_a_plane')
        self.assertEqual(to_snake_case('SnakesOnAPlane'), 'snakes_on_a_plane')
        self.assertEqual(to_snake_case('snakes_on_a_plane'), 'snakes_on_a_plane')
        self.assertEqual(to_snake_case('IPhoneHysteria'), 'i_phone_hysteria')
        self.assertEqual(to_snake_case('iPhoneHysteria'), 'i_phone_hysteria')

    def test_replace_non_alphabet(self):
        self.assertEqual(replace_non_alphabet('%#Start_with', '-'), '-Start-with')
        self.assertEqual(replace_non_alphabet('%#Start_with09++', '-'), '-Start-with09-')


class CaseInsensitiveDictTestCase(unittest.TestCase):
    possible_keys = ('accept', 'ACCEPT', 'aCcEpT', 'Accept')

    def setUp(self):
        """CaseInsensitiveDict instance with "Accept" header."""
        super().setUp()
        self.case_insensitive_dict = CaseInsensitiveDict()
        self.case_insensitive_dict['Accept'] = 'application/json'

    def test_list(self):
        self.assertEqual(list(self.case_insensitive_dict), ['Accept'])

    def test_getitem(self):
        for key in self.possible_keys:
            self.assertEqual(self.case_insensitive_dict[key], 'application/json')

    def test_delitem(self):
        for key in self.possible_keys:
            self.setUp()
            del self.case_insensitive_dict[key]
            self.assertNotIn(key, self.case_insensitive_dict)

    def test_lower_item(self):
        self.assertEqual(list(self.case_insensitive_dict.lower_items()), [('accept', 'application/json')])

    def test_repr(self):
        self.assertEqual(repr(self.case_insensitive_dict), "{'Accept': 'application/json'}")

    def test_copy(self):
        copy = self.case_insensitive_dict.copy()
        self.assertIsNot(copy, self.case_insensitive_dict)
        self.assertEqual(copy, self.case_insensitive_dict)

    def test_instance_equality(self):
        instances = (
            ({'AccePT': 'application/json'}, True),
            ({}, False),
            (None, False)
        )
        for item in instances:
            self.assertEqual((self.case_insensitive_dict == item[0]), item[1])


if __name__ == '__main__':  # pragma: nocover
    unittest.main()
