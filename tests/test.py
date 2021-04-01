from src import main

import pytest


def test_main():
    assert main.main() == 'Test'
