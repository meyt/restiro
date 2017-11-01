import unittest
from webtest_docgen.utils import to_snake_case, replace_non_alphabet


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


if __name__ == '__main__':  # pragma: nocover
    unittest.main()
