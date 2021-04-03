from src.config import TEST_DB_URI
from helpers import get_static_json_file
from helpers import mocked_get_request
from src import database
from src import monitor
from unittest import mock

import pytest
import requests


DATA = {
    "date": "3 hours ago",
    "title": "Example title",
    "topic": "Coronavirus",
    "url": "https://www.example.com"
}

PREVIOUS = {
    "date": "2 hours ago",
    "title": "Example title",
    "topic": "Pandemic",
    "url": "https://www.example.com"
}


@pytest.fixture(scope='function')
def news(*args, **kwargs):
    db = database.DBInterface(TEST_DB_URI)
    yield (db, monitor.SBSNewsMonitor(db))
    db.close()


@pytest.mark.parametrize('event, element, previous, res', [
    ('added', 'article', None, {
        'event': 'added',
        'element': 'article',
        'contents': DATA
    }),
    ('updated', 'section', None, {
        'event': 'updated',
        'element': 'section',
        'contents': DATA
    }),
    ('updated', 'section', PREVIOUS, {
        'event': 'updated',
        'element': 'section',
        'contents': DATA,
        'previous_contents': PREVIOUS
    }),
    ('removed', 'link', None, {
        'event': 'removed',
        'element': 'link',
        'contents': DATA
    })
])
def test_describe_change(news, event, element, previous, res):
    __, sbs = news
    if previous:
        assert sbs.describe_change(event, element, DATA, previous) == res
    else:
        assert sbs.describe_change(event, element, DATA) == res


def test_update(news):
    __, sbs = news
    with mock.patch('requests.get') as mocked_request:
        mocked_request.side_effect = lambda url: \
            mocked_get_request(url, mock='news-v1.html')
        assert sbs.update() == get_static_json_file('initial.json')
        mocked_request.side_effect = lambda url: \
            mocked_get_request(url, mock='news-v2.html')
        assert sbs.update() == get_static_json_file('changes.json')


class FakeNewsMonitor(monitor.NewsMonitor):
    """Monitor a fake news web page."""

    def __init__(self, db):
        """
        Class constructor.

        :param DBInterface db: the database interface
        """
        super().__init__()
        self.db = db
        self.url = 'https://www.fake-news.com'
        self.items = [
            {
                'item_type': 'dummy-placeholder',
                'item_selector': 'fake-section',
                'metadata_selectors': [
                    {'name': 'title', 'class': 'fake-metadata'}
                ]
            }
        ]


def test_multi_news(news):
    db, __ = news
    fake_news = FakeNewsMonitor(db)
    with mock.patch('requests.get') as mocked_request:
        mocked_request.side_effect = lambda url: \
            mocked_get_request(url, mock='fake-news.html')
        assert fake_news.update() == get_static_json_file('fake-news.json')
