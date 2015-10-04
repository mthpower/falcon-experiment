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

    # Try to delete anyway, in case we did not in the test
    client.delete(path, content_type='application/json')


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
    not_found_response = client.get(user)
    assert not_found_response.status == '404 Not Found'


def test_delete_user_not_found(client):
    response = client.delete('/user/does-not-exist')
    assert response.status == '404 Not Found'
    assert response.data == b''
