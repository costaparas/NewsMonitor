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

        Items are scraped on the basis of selection by CSS class.

        Metadata can be scraped in the following currently supported ways:
          - selecting an element by CSS class within the scraped item
          - selecting an element by tag name within the scraped item

        In either case, the extracted metadata may either be:
            - the text content in the element
            - the value of a HTML attribute in the element

        :param BeautifulSoup soup: object derived from the web page
        :return list: key-value pairs of metadata from the scraped items
        """
        self.raw_data = soup.find_all(class_=self.item_selector)
        for e in self.raw_data:
            item = {}
            for selector in self.metadata_selectors:
                if 'class' in selector:
                    data = e.find(class_=selector['class'])
                    if data and 'tag' in selector and 'attr' in selector:
                        # search for tag & extract HTML attribute
                        data = data.find(selector['tag'])
                        if data:
                            item[selector['name']] = data[selector['attr']]
                    elif data:
                        # extract text data from HTML element
                        item[selector['name']] = data.text.strip()
                elif 'tag' in selector:
                    data = e.find(selector['tag'])
                    if data and 'attr' in selector:
                        # select by HTML tag and extract HTML attribute
                        item[selector['name']] = data[selector['attr']]
                    elif data:
                        # select by HTML tag only
                        item[selector['name']] = data.text.strip()
            if item and item not in self.content:
                self.content.append(item)
        return self.content
