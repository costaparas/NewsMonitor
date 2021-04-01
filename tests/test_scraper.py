from bs4 import BeautifulSoup
from src import scraper
from unittest import mock

import os
import pytest
import requests


def mocked_get_request(url):
    """
    Mock perform a GET request for a file.

    :param string url: name of file to use a response content
    :return MockResponse: mocked GET response
    """
    class MockResponse:
        """Mock class for a GET response."""

        def __init__(self, url):
            parent = os.path.dirname(os.path.realpath(__file__))
            filepath = os.path.join(parent, 'data', url)
            if os.path.isfile(filepath):
                with open(filepath) as f:
                    self.content = ''.join(f.readlines())
            else:
                self.content = b'Placeholder Content'

    return MockResponse(url)


@pytest.mark.parametrize('url', ['news-v1.html'])
def test_scraper(url):
    with mock.patch('requests.get') as mocked_request:
        mocked_request.side_effect = mocked_get_request
        soup = BeautifulSoup(requests.get(url).content, 'html.parser')

    item_selector = 'page__section page__section--style-1'
    metadata_selectors = [
        {'value': 'block__title', 'name': 'title'}
    ]

    s = scraper.ItemScraper(item_selector, metadata_selectors)
    items = s.scrape(soup)
    assert items == [
        {'title': 'Vaccine in Focus'},
        {'title': 'SBS News Explains'},
        {'title': 'News from around SBS'},
        {'title': "Editor's Choice"},
        {'title': 'Investigations'}
    ]
