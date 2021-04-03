from bs4 import BeautifulSoup
from helpers import get_static_filepath
from helpers import get_static_json_file
from src import scraper

import json
import pytest


@pytest.fixture(scope='function')
def webpage(*args, **kwargs):
    content = ''.join(open(get_static_filepath('news-v1.html')).readlines())
    return BeautifulSoup(content, 'html.parser')


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
