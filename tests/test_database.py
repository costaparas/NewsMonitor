from src import database
from src.config import TEST_DB_URI

import pytest


@pytest.fixture(scope='function')
def db(*args, **kwargs):
    db_interface = database.DBInterface(TEST_DB_URI)
    yield db_interface
    db_interface.close()


@pytest.fixture(scope='function')
def insert_data(*args, **kwargs):
    return {
        'title': None,
        'item_type': 'dummy item type',
        'present': True,
        'news_source': 'https://www.dummy-source.com'
    }


@pytest.fixture(scope='function')
def result_data(*args, **kwargs):
    return {
        'tracked_item_id': None,
        'title': None,
        'url': None,
        'date': None,
        'topic': None,
        'item_type': 'dummy item type',
        'news_source': 'https://www.dummy-source.com',
        'present': True
    }


def test_database_1_item(db, insert_data, result_data):
    insert_data['title'] = 'dummy title 1'
    insert_data['topic'] = 'a dummy topic'
    db.insert_item(insert_data)
    items = db.get_items(insert_data['item_type'], insert_data['news_source'])
    assert len(items) == 1
    result_data['title'] = insert_data['title']
    result_data['topic'] = 'a dummy topic'
    result_data['tracked_item_id'] = 1
    assert db.tuple_to_dict(items[0]) == result_data


def test_tuple_to_dict(db, insert_data, result_data):
    result_data['title'] = 'dummy title 1'
    result_data['topic'] = 'a dummy topic'
    result_data['tracked_item_id'] = 1
    items = db.get_items(insert_data['item_type'], insert_data['news_source'])

    # show primary key, omit `topic`
    del result_data['topic']
    assert db.tuple_to_dict(items[0], False, ['topic']) == result_data

    # hide primary key, show `topic`
    del result_data['tracked_item_id']
    result_data['topic'] = 'a dummy topic'
    assert db.tuple_to_dict(items[0], True, []) == result_data

    # hide primary key, omit `topic`
    del result_data['topic']
    assert db.tuple_to_dict(items[0], True, ['topic']) == result_data


def test_update(db, insert_data, result_data):
    result_data['title'] = 'dummy title 1'
    result_data['tracked_item_id'] = 1
    items = db.get_items(insert_data['item_type'], insert_data['news_source'])
    items[0].update(db.tuple_to_dict(items[0]), result_data)
    assert db.tuple_to_dict(items[0]) == result_data


def test_database_2_items(db, insert_data, result_data):
    insert_data['title'] = 'dummy title 2'
    db.insert_item(insert_data)
    items = db.get_items(insert_data['item_type'], insert_data['news_source'])
    assert len(items) == 2
    for i, item in enumerate(items, 1):
        result_data['title'] = f'dummy title {i}'
        result_data['tracked_item_id'] = i
        assert db.tuple_to_dict(item) == result_data
