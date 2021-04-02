from abc import ABC
from bs4 import BeautifulSoup
from scraper import ItemScraper

import requests


class NewsMonitor(ABC):
    """Monitor a news web page."""

    def __init__(self):
        """
        Class constructor.

        Any derived class should define a `url` string and an `items`
        list of dicts.

        The `url` is the web page to monitor.

        Each element of the `items` list should define the following keys:
        - `item_type`: a string representing the type of item to monitor
        - `item_selector`: the CSS class of the item being monitored
        - `metadata_selectors`: list of dicts of metadata selectors

        Each metadata selector should define keys as described in
        :func:`~scraper.ItemScraper.scrape`.
        """
        pass

    def update(self):
        """
        Check and report changes to tracked items on the web page.

        :return list: a list of dictionaries, each describing a change to one
                element specific item on the page
        """
        changes = []
        page = requests.get(self.url).content
        soup = BeautifulSoup(page, 'html.parser')
        for item in self.items:
            scraper = ItemScraper(item['item_selector'],
                                  item['metadata_selectors'])
            current_items = scraper.scrape(soup)
            for i in self.db.get_items(item['item_type'], self.url):
                item_dict = self.db.tuple_to_dict(i, True,
                                                  ['item_type', 'present',
                                                   'news_source'])
                current = [e for e in current_items if e['title'] == i.title]
                if len(current):
                    if i.update(i, item_dict, current[0]):  # possibly update
                        changes.append(self.describe_change('updated',
                                       item['item_type'], current[0],
                                       item_dict))
                    i.news_source = self.url
                    current_items.remove(current[0])  # discard once processed
                elif i.present:
                    changes.append(self.describe_change('removed',
                                   item['item_type'], item_dict))
                    i.present = False  # item has been removed

            # add any remaining items for the first time
            for e in current_items:
                changes.append(self.describe_change('added',
                               item['item_type'], e.copy()))
                e['present'] = True
                e['item_type'] = item['item_type']
                e['news_source'] = self.url
                self.db.insert_item(e)

        self.db.session.commit()
        return changes

    def describe_change(self, event, item_type, data, previous_data=None):
        """
        Generate a human-readable dictionary describing the change.

        :param string event: the event type, e.g. "added", "removed"
        :param string item_type: the type of item, e.g. "article", "section"
        :param dict data: the current data visible on the web page
        :param dict previous_data: the data previously recorded; if omitted,
               the field will be suppressed from the output
        :return dict: description of the update
        """
        def normalize(data):
            """Order the keys and remove null values."""
            return {key: data[key] for key in sorted(data) if data[key]}

        description = {
            'event': event,
            'element': item_type,
            'contents': normalize(data)
        }

        if previous_data:
            description['previous_contents'] = normalize(previous_data)

        return description


class SBSNewsMonitor(NewsMonitor):
    """Monitor an SBS news web page."""

    def __init__(self, db):
        """
        Class constructor.

        :param DBInterface db: the database interface
        """
        super().__init__()
        self.db = db
        self.url = 'https://www.sbs.com.au/news/'
        self.items = [
            {
                'item_type': 'section',
                'item_selector': 'page__section page__section--style-1',
                'metadata_selectors': [
                    {'name': 'title', 'class': 'block__title'}
                ],
            },
            {
                'item_type': 'article',
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
                'item_type': 'link',
                'item_selector': 'menu__list-item',
                'metadata_selectors': [
                    {'name': 'title', 'tag': 'a'},
                    {'name': 'url', 'tag': 'a', 'attr': 'href'}
                ]
            }
        ]
