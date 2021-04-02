from bs4 import BeautifulSoup
from src import scraper
from unittest import mock

import json
import os
import pytest
import requests


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


def mocked_get_request(url):
    """
    Mock perform a GET request for a file.

    :param string url: name of file to use a response content
    :return MockResponse: mocked GET response
    """
    class MockResponse:
        """Mock class for a GET response."""

        def __init__(self, url):
            filepath = get_static_filepath(url)
            if filepath:
                with open(filepath) as f:
                    self.content = ''.join(f.readlines())
            else:
                self.content = b'Placeholder Content'

    return MockResponse(url)


@pytest.fixture(scope='function')
def webpage(*args, **kwargs):
    url = 'news-v1.html'
    with mock.patch('requests.get') as mocked_request:
        mocked_request.side_effect = mocked_get_request
        soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    return soup


def test_section_scraping(webpage):
    s = scraper.ItemScraper(
        'page__section page__section--style-1',
        [{'name': 'title', 'class': 'block__title'}]
    )
    items = s.scrape(webpage)
    assert items == get_static_json_file('sections.json')


def test_article_scraping(webpage):
    s = scraper.ItemScraper(
        'preview',
        [
            {'name': 'topic', 'class': 'topic__string'},
            {'name': 'title', 'class': 'preview__headline'},
            {'name': 'date', 'class': 'date__string'},
            {'name': 'url', 'class': 'preview__headline',
             'tag': 'a', 'attr': 'href'}
        ]
    )
    items = s.scrape(webpage)
    assert items == get_static_json_file('articles.json')


def test_list_scraping(webpage):
    s = scraper.ItemScraper(
        'menu__list-item',
        [
            {'name': 'title', 'tag': 'a'},
            {'name': 'url', 'tag': 'a', 'attr': 'href'}
        ]
    )
    items = s.scrape(webpage)
    assert items == get_static_json_file('lists.json')
