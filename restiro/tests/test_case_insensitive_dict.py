import pytest
from restiro.helpers import CaseInsensitiveDict

# original source from `requests` library


@pytest.fixture(autouse=True)
def case_insensitive_dict():
    """CaseInsensitiveDict instance with "Accept" header."""
    case_insensitive_dict = CaseInsensitiveDict()
    case_insensitive_dict['Accept'] = 'application/json'
    return case_insensitive_dict


def test_list(case_insensitive_dict):
    assert list(case_insensitive_dict) == ['Accept']


possible_keys = pytest.mark.parametrize('key', ('accept', 'ACCEPT', 'aCcEpT', 'Accept'))


@possible_keys
def test_getitem(case_insensitive_dict, key):
    assert case_insensitive_dict[key] == 'application/json'


@possible_keys
def test_delitem(case_insensitive_dict, key):
    del case_insensitive_dict[key]
    assert key not in case_insensitive_dict


def test_lower_items(case_insensitive_dict):
    assert list(case_insensitive_dict.lower_items()) == [('accept', 'application/json')]


def test_repr(case_insensitive_dict):
    assert repr(case_insensitive_dict) == "{'Accept': 'application/json'}"


def test_copy(case_insensitive_dict):
    copy = case_insensitive_dict.copy()
    assert copy is not case_insensitive_dict
    assert copy == case_insensitive_dict


@pytest.mark.parametrize(
    'other, result', (
        ({'AccePT': 'application/json'}, True),
        ({}, False),
        (None, False)
    )
)
def test_instance_equality(case_insensitive_dict, other, result):
    assert (case_insensitive_dict == other) is result
