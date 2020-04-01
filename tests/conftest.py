import pytest

import requests
from flask import url_for

from bookapp import create_app
from bookapp.models import db, Book, BookRequest
from configs.config import TestConfig


@pytest.fixture(scope='session')
def app():
    app = create_app(TestConfig)
    return app
