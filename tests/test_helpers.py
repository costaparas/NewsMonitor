from helpers import get_static_filepath
from helpers import get_static_json_file
from helpers import mocked_get_request

import pytest


def test_static_filepath():
    with pytest.raises(ValueError) as e:
        get_static_filepath('not_a_file.txt')


def test_static_json_file():
    assert get_static_json_file('not_a_file.json') == []


def test_mocked_get_request():
    content = ''.join(open(get_static_filepath('lists.json')).readlines())
    assert mocked_get_request('lists.json').content == content

    with pytest.raises(ValueError) as e:
        mocked_get_request('not_a_file.txt')
