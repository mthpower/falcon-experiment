#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for the group endpoints."""

import json
from urllib.parse import urlparse

import pytest


@pytest.yield_fixture()
def group(client):
    """Fixture to yield a relative uri of a created group."""
    payload = json.dumps({
        'name': 'Test Group',
    })
    response = client.post(
        '/group', data=payload, content_type='application/json'
    )
    body = json.loads(response.data.decode())
    parsed_url = urlparse(body['uri'])
    path = parsed_url.path
    yield path

    # Try to delete anyway, in case we did not in the test
    client.delete(path, content_type='application/json')


@pytest.yield_fixture()
def users(client):
    """Fixture to yield a list of relative uris to created users."""
    usernames = [
        ('A Test', 'a.test@example.com'),
        ('B Test', 'b.test@example.com'),
        ('C Test', 'c.test@example.com'),
    ]
    paths = []
    for username, email in usernames:
        payload = json.dumps({
            'name': username,
            'email': email,
        })
        response = client.post(
            '/user', data=payload, content_type='application/json'
        )
        body = json.loads(response.data.decode())
        parsed_url = urlparse(body['uri'])
        path = parsed_url.path
        paths.append(path)

    yield paths

    for path in paths:
        teardown_resp = client.delete(path, content_type='application/json')
        if not teardown_resp.status == '204 No Content':
            raise Exception


def test_post_group(client):
    """Test that we can create a group.

    Tests that a group can be created by making a POST request to the
    group collection endpoint.
    """
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
    """Test that a bad payload returns a HTTP Bad Request.

    In this case, when creating a group, we've incorrectly spelt a required key
    of the JSON.
    """
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
    """Test that a group can be retrieved.

    Tests that a group can be retrieved by making a GET request to the URI
    of a group.
    """
    response = client.get(group)
    assert response.status == '200 OK'
    body = json.loads(response.data.decode())
    assert body['name'] == 'Test Group'
    assert body['created']


def test_get_group_not_found(client):
    """Test that a group that does not exist returns a HTTP Not Found."""
    response = client.get('/group/does-not-exist')
    assert response.status == '404 Not Found'
    assert response.data == b''


def test_delete_group(client, group):
    """Test that a group can be deleted.

    Tests that a group can be deleted by making a DELETE request to the URI
    of the group.
    """
    response = client.delete(group)
    assert response.status == '204 No Content'
    assert response.data == b''
    not_found_response = client.get(group)
    assert not_found_response.status == '404 Not Found'


def test_delete_group_not_found(client):
    """Test deleting a group that does not exist.

    A DELETE request for a group that does not exist should return an
    HTTP Not Found.
    """
    response = client.delete('/group/does-not-exist')
    assert response.status == '404 Not Found'
    assert response.data == b''


# Testing user relations
# def test_post_group_with_users(client, users):
#     payload = json.dumps({
#         'name': 'Test Group with Users',
#         'users': users
#     })
#     response = client.post(
#         '/group', data=payload, content_type='application/json'
#     )
#     body = json.loads(response.data.decode())
#     parsed_url = urlparse(body['uri'])
#     path = parsed_url.path

#     assert response.status == '201 Created'

#     group_response = client.get(path, content_type='application/json')
#     body = json.loads(group_response.data.decode())
#     assert group_response.status == '200 OK'
#     assert body['users'] == users
