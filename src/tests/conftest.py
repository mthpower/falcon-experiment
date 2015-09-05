#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from werkzeug.test import Client
from werkzeug.wrappers import BaseResponse

from falcon_experiment import app
from falcon_experiment.db import db_client, delete_all


@pytest.yield_fixture
def db(scope='session'):
    yield db_client
    # Remove all keys from the db after the test run, just in case.
    delete_all()


@pytest.yield_fixture
def client(db):
    yield Client(app.application, BaseResponse)
