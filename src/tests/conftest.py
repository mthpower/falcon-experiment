#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from werkzeug.test import Client
from werkzeug.wrappers import BaseResponse

from falcon_experiment import app
from falcon_experiment import models
from falcon_experiment.db import engine


@pytest.yield_fixture
def db(scope='session'):
    """
    Ensure database is set up before every test run,
    and is torn down at the end.
    """
    models.Model.metadata.create_all(engine)
    yield
    models.Model.metadata.drop_all(engine)


@pytest.yield_fixture
def client(db):
    yield Client(app.application, BaseResponse)
