#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from falcon_experiment.db import db_client, delete_all


@pytest.yield_fixture
def db(scope='session'):
    yield db_client
    delete_all()
