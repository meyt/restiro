import pytest

from os import makedirs
from shutil import rmtree
from restiro.tests.helpers import temp_dir


@pytest.fixture('module', autouse=True)
def wrap_directories():
    rmtree(temp_dir, ignore_errors=True)
    makedirs(temp_dir, exist_ok=True)
    yield True
    rmtree(temp_dir, ignore_errors=True)
