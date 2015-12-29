# -*- coding: utf-8 -*-
"""Global test configuration using pytest's conftest.py standard."""
import pytest

from werkzeug.test import Client
from werkzeug.wrappers import BaseResponse

from falcon_experiment import app
from falcon_experiment import models
from falcon_experiment.db import engine


@pytest.yield_fixture
def db(scope='session'):
    """Ensure database is set up and torn down every test run."""
    models.Model.metadata.create_all(engine)
    yield
    models.Model.metadata.drop_all(engine)


@pytest.yield_fixture
def client(db):
    """Provide a client using werkzeug for simulating HTTP."""
    yield Client(app.application, BaseResponse)
