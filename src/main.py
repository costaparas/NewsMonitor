from bs4 import BeautifulSoup
from database import DBInterface
from scraper import ItemScraper

import requests


DB_URI = 'sqlite:///news.db'


class NewsMonitor:

    def __init__(self, db):
        self.db = db
        self.url = 'https://www.sbs.com.au/news/'
        self.items = [
            {
                'item_selector': 'page__section page__section--style-1',
                'metadata_selectors': [
                    {'name': 'title', 'class': 'block__title'}
                ],
            },
            {
                'item_selector': 'preview',
                'metadata_selectors': [
                    {'name': 'topic', 'class': 'topic__string'},
                    {'name': 'title', 'class': 'preview__headline'},
                    {'name': 'date', 'class': 'date__string'},
                    {'name': 'url', 'class': 'preview__headline',
                     'tag': 'a', 'attr': 'href'}
                ]
            },
            {
                'item_selector': 'menu__list-item',
                'metadata_selectors': [
                    {'name': 'topic', 'tag': 'a'},
                    {'name': 'url', 'tag': 'a', 'attr': 'href'}
                ]
            }
        ]

    def update(self):

        page = requests.get(self.url).content
        soup = BeautifulSoup(page, 'html.parser')

        item_selector = self.items[0]['item_selector']
        metadata_selectors = self.items[0]['metadata_selectors']

        section_scraper = ItemScraper(item_selector, metadata_selectors)
        section_items = section_scraper.scrape(soup)
        print(section_items)
        for item in section_items:
            item['present'] = True
            item['item_type'] = 'section'
            self.db.insert_item(item)
        for item in self.db.get_items('section'):
            print(self.db.tuple_to_dict(item))


def main():
    """Program entrypoint."""
    db = DBInterface(DB_URI)
    monitor = NewsMonitor(db)
    monitor.update()
    db.close()


if __name__ == '__main__':
    main()
