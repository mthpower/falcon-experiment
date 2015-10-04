#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from urllib.parse import urlparse

import pytest


@pytest.yield_fixture()
def user(client):
    payload = json.dumps({
        'username': 'A Test',
        'email': 'a.test@example.com'
    })
    response = client.post(
        '/user', data=payload, content_type='application/json'
    )
    body = json.loads(response.data.decode())
    parsed_url = urlparse(body['uri'])
    path = parsed_url.path
    yield path

    teardown_resp = client.delete(path, content_type='application/json')
    if not teardown_resp.status == '204 No Content':
        raise Exception


def test_post_user(client):
    payload = json.dumps({
        'username': 'A Test',
        'email': 'a.test@example.com'
    })
    response = client.post(
        '/user', data=payload, content_type='application/json'
    )
    body = json.loads(response.data.decode())
    assert response.status == '201 Created'
    assert body['uri'] == 'http://localhost:8000/user/a.test@example.com'


def test_post_user_bad_request(client):
    payload = json.dumps({
        'username': 'A Test',
        # Wrong key name!
        'emial': 'a.test@example.com'
    })
    response = client.post(
        '/user', data=payload, content_type='application/json'
    )
    body = json.loads(response.data.decode())
    assert response.status == '400 Bad Request'
    assert body['title'] == 'Invalid document submitted'
    assert body['description'] == {
        'email': ['Missing data for required field.']
    }


def test_get_user(client, user):
    response = client.get(user)
    assert response.status == '200 OK'
    body = json.loads(response.data.decode())
    assert body['username'] == 'A Test'
    assert body['email'] == 'a.test@example.com'
    assert body['created']


def test_get_user_not_found(client):
    response = client.get('/user/does-not-exist')
    assert response.status == '404 Not Found'
    assert response.data == b''


def test_delete_user(client, user):
    response = client.delete(user)
    assert response.status == '204 No Content'
    assert response.data == b''


def test_delete_user_not_found(client):
    response = client.delete('/user/does-not-exist')
    assert response.status == '404 Not Found'
    assert response.data == b''
