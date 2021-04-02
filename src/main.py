from bs4 import BeautifulSoup
from database import DBInterface
from scraper import ItemScraper

import requests


db_uri = 'sqlite:///news.db'
url = 'https://www.sbs.com.au/news/'


def main():
    """Program entrypoint."""
    db = DBInterface(db_uri)

    page = requests.get(url).content
    soup = BeautifulSoup(page, 'html.parser')

    item_selector = 'page__section page__section--style-1'
    metadata_selectors = [
        {'name': 'title', 'class': 'block__title'}
    ]

    section_scraper = ItemScraper(item_selector, metadata_selectors)
    section_items = section_scraper.scrape(soup)
    print(section_items)
    for item in section_items:
        item['present'] = True
        item['item_type'] = 'section'
        db.insert_item(item)
    for item in db.get_items('section'):
        print(db.tuple_to_dict(item))
    db.close()


if __name__ == '__main__':
    main()
