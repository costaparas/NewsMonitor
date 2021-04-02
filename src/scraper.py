class ItemScraper:
    """Scrape related items on a web page."""

    def __init__(self, item_selector, metadata_selectors):
        """
        Class constructor.

        :param string item_selector: CSS class of items to select
        :param dict metadata_selectors: name of fields to select within
               each item and selectors to use for extracting them
        """
        self.item_selector = item_selector
        self.metadata_selectors = metadata_selectors
        self.content = []

    def scrape(self, soup):
        """
        Find and return all requested items from the page.

        :param BeautifulSoup soup: object derived from the web page
        :return list: key-value pairs of metadata from the scraped items
        """
        self.raw_data = soup.find_all(class_=self.item_selector)
        for e in self.raw_data:
            item = {}
            for selector in self.metadata_selectors:
                data = e.find(class_=selector['class'])
                if data and 'tag' in selector and 'attr' in selector:
                    # search for tag & extract HTML attribute
                    data = data.find(selector['tag'])
                    if data:
                        item[selector['name']] = data[selector['attr']]
                elif data:
                    # extract text data from element
                    item[selector['name']] = data.text.strip()
            if item:
                self.content.append(item)
        return self.content
