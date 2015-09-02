#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from werkzeug.test import Client
from werkzeug.wrappers import BaseResponse

from falcon_experiment import app


@pytest.yield_fixture
def client():
    yield Client(app.application, BaseResponse)


def test_get_user_collection(client):
    response = client.get('/users')
    assert response.status == '200 OK'


def test_get_job_detail(client):
    response = client.get('/users/Alice')
    assert response.status == '200 OK'
