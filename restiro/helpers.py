
import re
import collections
import tempfile

from os import makedirs
from os.path import join
from shutil import rmtree

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


def get_examples_dir():
    temp_dir = join(tempfile.gettempdir(), 'restiro_examples')
    makedirs(temp_dir, exist_ok=True)
    return temp_dir


def clean_examples_dir():
    rmtree(get_examples_dir())


class CaseInsensitiveDict(collections.MutableMapping):
    """A case-insensitive ``dict``-like object.

    Implements all methods and operations of
    ``collections.MutableMapping`` as well as dict's ``copy``. Also
    provides ``lower_items``.

    All keys are expected to be strings. The structure remembers the
    case of the last key to be set, and ``iter(instance)``,
    ``keys()``, ``items()``, ``iterkeys()``, and ``iteritems()``
    will contain case-sensitive keys. However, querying and contains
    testing is case insensitive::

        cid = CaseInsensitiveDict()
        cid['Accept'] = 'application/json'
        cid['aCCEPT'] == 'application/json'  # True
        list(cid) == ['Accept']  # True

    For example, ``headers['content-encoding']`` will return the
    value of a ``'Content-Encoding'`` response header, regardless
    of how the header name was originally stored.

    If the constructor, ``.update``, or equality comparison
    operations are given keys that have equal ``.lower()``s, the
    behavior is undefined.
    """

    def __init__(self, data=None, **kwargs):
        self._store = collections.OrderedDict()
        if data is None:
            data = {}
        self.update(data, **kwargs)

    def __setitem__(self, key, value):
        # Use the lower-cased key for lookups, but store the actual
        # key alongside the value.
        self._store[key.lower()] = (key, value)

    def __getitem__(self, key):
        return self._store[key.lower()][1]

    def __delitem__(self, key):
        del self._store[key.lower()]

    def __iter__(self):
        return (cased_key for cased_key, mapped_value in self._store.values())

    def __len__(self):
        return len(self._store)

    def lower_items(self):
        """Like iteritems(), but with all lowercase keys."""
        return (
            (lower_key, key_val[1])
            for (lower_key, key_val)
            in self._store.items()
        )

    def __eq__(self, other):
        if isinstance(other, collections.Mapping):
            other = CaseInsensitiveDict(other)
        else:
            return NotImplemented
        # Compare insensitively
        return dict(self.lower_items()) == dict(other.lower_items())

    # Copy is required
    def copy(self):
        return CaseInsensitiveDict(self._store.values())

    def __repr__(self):
        return str(dict(self.items()))
