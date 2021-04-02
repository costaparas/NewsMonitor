from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class TrackedItem(Base):
    """
    Item found on a web page being scraped.

    Metadata about the item is stored, along with its "type" and a flag
    to indidate whehter its currently on the page.
    """

    __tablename__ = "tracked_item"

    # w.l.o.g items can be distinguished by their "title"
    # but a numeric primary key is also used
    tracked_item_id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)

    # optional fields, which may apply to some items
    url = Column(String)
    date = Column(String)
    topic = Column(String)

    # "article", "link", "section", etc
    item_type = Column(String, nullable=False)

    # True if the item is currently on the page
    # False if the item was previously on the page
    present = Column(Boolean, nullable=False)

    def __init__(self, title, item_type, present,
                 url=None, date=None, topic=None):
        """
        Class constructor.

        :param string title: the distinct item title
        :param string item_type: the type of item
        :param boolean present: True if present on the page; False otherwise
        :param string url: the associated url, if applicable
        :param string date: the associated date/time, if applicable
        :param string topic: the associated topic, if applicable
        """
        self.title = title
        self.item_type = item_type
        self.present = present
        self.url = url
        self.date = date
        self.topic = topic

    def update(self, db_tuple, tuple_data, new_data):
        """
        Update database tuple with new data.

        :param database.Table db_tuple: existing database tuple
        :param dict tuple_data: existing data as a dict
        :param dict new_data: current data to update with
        :return boolean: True if the tuple was updated;
                False if no update was needed (data unchanged)
        """
        changed = False
        for col, val in tuple_data.items():
            if val is not None and col in new_data:
                if val != new_data[col]:
                    setattr(db_tuple, col, new_data[col])
                    changed = True
            elif val is not None and col not in new_data:
                setattr(db_tuple, col, None)
                changed = True
            elif val is None and col in new_data:
                setattr(db_tuple, col, new_data[col])
                changed = True
        return changed


class DBInterface:
    """Interact with database."""

    def __init__(self, db_uri):
        """
        Class constructor.

        :param string db_uri: the location of the database
        """
        self.db_engine = create_engine(db_uri)
        self.conn = self.db_engine.connect()
        Session = sessionmaker()
        Session.configure(bind=self.db_engine)
        self.session = Session()

        # create empty db tables on first run
        try:
            self.session.query(TrackedItem).first()
        except OperationalError:
            Base.metadata.create_all(self.db_engine,
                                     Base.metadata.tables.values(),
                                     checkfirst=True)
        self.is_open = True

    def get_items(self, item_type):
        """
        Return items of specified type.

        :param string item_type: the item type to retrieve
        :return list: items retrieved from the database
        """
        return self.session.query(
            TrackedItem
        ).filter_by(item_type=item_type).all()

    def insert_item(self, item):
        """
        Add item to database.

        :param dict item: the data to add to the database
        """
        for field in ['url', 'date', 'topic']:
            if field not in item:  # insert dummy optional fields
                item[field] = None
        new_item = TrackedItem(title=item['title'],
                               item_type=item['item_type'],
                               present=item['present'],
                               url=item['url'],
                               date=item['date'],
                               topic=item['topic'])
        self.session.add(new_item)
        self.session.commit()

    def tuple_to_dict(self, row, skip_pk=False, skip_cols=[]):
        """
        Convert database tuple into a Python dictionary.

        :param database.Table row: source database tuple
        :param boolean skip_pk: True if primary key should be
               skipped; False otherwise
        :param list skip_cols: columns to skip
        :return dict: dictionary containing the data
        """
        ret = {}
        for c in row.__table__.columns:
            if c.name not in skip_cols and (not skip_pk or not c.primary_key):
                ret[c.name] = getattr(row, c.name)
        return ret

    def close(self):
        """Close any open resources."""
        if self.is_open:
            self.session.commit()
            self.session.close()
            self.conn.close()
            self.is_open = False
