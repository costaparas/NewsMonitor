from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy import insert
from sqlalchemy import update
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
            self.session.query(TrackedItem).one()
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

    def close(self):
        """Close any open resources."""
        if self.is_open:
            self.session.commit()
            self.session.close()
            self.conn.close()
            self.is_open = False
