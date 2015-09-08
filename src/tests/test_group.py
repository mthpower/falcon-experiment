#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from urllib.parse import urlparse

import pytest


@pytest.yield_fixture()
def group(client):
    payload = json.dumps({
        'name': 'Test Group',
    })
    response = client.post(
        '/group', data=payload, content_type='application/json'
    )
    body = json.loads(response.data.decode())
    parsed_url = urlparse(body['uri'])
    yield parsed_url.path
    # TODO: teardown


def test_post_group(client):
    payload = json.dumps({
        'name': 'A Test',
    })
    response = client.post(
        '/group', data=payload, content_type='application/json'
    )
    body = json.loads(response.data.decode())
    assert response.status == '201 Created'
    assert body['uri']


def test_post_group_bad_request(client):
    payload = json.dumps({
        # Wrong key name!
        'naem': 'A Test',
    })
    response = client.post(
        '/group', data=payload, content_type='application/json'
    )
    body = json.loads(response.data.decode())
    assert response.status == '400 Bad Request'
    assert body['title'] == 'Invalid document submitted'
    assert body['description'] == {
        'name': ['Missing data for required field.']
    }


def test_get_group(client, group):
    response = client.get(group)
    assert response.status == '200 OK'
    body = json.loads(response.data.decode())
    assert body['name'] == 'Test Group'
    assert body['created_at']


def test_get_group_not_found(client):
    response = client.get('/group/does-not-exist')
    assert response.status == '404 Not Found'
    assert response.data == b''


def test_delete_group(client, group):
    response = client.delete(group)
    assert response.status == '204 No Content'
    assert response.data == b''


def test_delete_group_not_found(client):
    response = client.delete('/group/does-not-exist')
    assert response.status == '404 Not Found'
    assert response.data == b''
