from bs4 import BeautifulSoup
from scraper import ItemScraper

import requests


def main():
    url = 'https://www.sbs.com.au/news/'
    page = requests.get(url).content
    soup = BeautifulSoup(page, 'html.parser')

    item_selector = 'page__section page__section--style-1'
    metadata_selectors = [
        {'value': 'block__title', 'name': 'title'}
    ]

    section_scraper = ItemScraper(item_selector, metadata_selectors)
    section_items = section_scraper.scrape(soup)
    print(section_items)
    return 'Test'


if __name__ == '__main__':
    main()
