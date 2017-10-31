
import re


_under_scorer1 = re.compile(r'(.)([A-Z][a-z]+)')
_under_scorer2 = re.compile('([a-z0-9])([A-Z])')
_non_alphabet = re.compile('[\x00-\x2F\x3A-\x40\x5B-\x60\x7B-\x7F]+')


def to_snake_case(s):
    """ 
    Convert camelCase to snake_case
    """
    subbed = _under_scorer1.sub(r'\1_\2', s)
    return _under_scorer2.sub(r'\1_\2', subbed).lower()


def replace_non_alphabet(string, replace):
    """
    Replace non-alphabetic characters
    """
    return _non_alphabet.sub(replace, string)
