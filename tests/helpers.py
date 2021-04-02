import json
import os
import re


def get_static_filepath(filename):
    """
    Get local filepath for a static test file.

    :param string filename: name of file to retrieve
    :return dict: the filepath relative to the testing directory
    :raises ValueError: if file cannot be found
    """
    parent = os.path.dirname(os.path.realpath(__file__))
    filepath = os.path.join(parent, 'data', filename)
    if os.path.isfile(filepath):
        return filepath
    raise ValueError('Cannot find file')


def get_static_json_file(filename):
    """
    Return file contents of a static JSON file.

    :param string filename: name of file to retrieve
    :return list: the static JSON data
    """
    try:
        filepath = get_static_filepath(filename)
        with open(filepath) as f:
            return json.load(f)
    except ValueError:
        return []


def mocked_get_request(url, **kwargs):
    """
    Mock perform a GET request for a file.

    :param string url: name of file to use a response content
    :return MockResponse: mocked GET response
    """
    class MockResponse:
        """Mock class for a GET response."""

        def __init__(self, url, **kwargs):
            if 'mock' in kwargs:
                find = kwargs['mock']  # mocked file
            else:
                find = url  # static file
            filepath = get_static_filepath(find)
            with open(filepath) as f:
                self.content = ''.join(f.readlines())

    return MockResponse(url, **kwargs)
