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
    """Fixture to yield a list of emails to created users."""
    document = [
        {'email': 'a.test@example.com', 'username': 'A Test'},
        {'email': 'b.test@example.com', 'username': 'B Test'},
        {'email': 'c.test@example.com', 'username': 'C Test'},
    ]
    for user in document:
        client.post(
            '/user', data=json.dumps(user), content_type='application/json'
        )

    yield [{'email': user['email']} for user in document]

    for user in document:
        client.delete(
            '/user/{}'.format(user['email']), content_type='application/json'
        )


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


def test_post_group_with_users(client, users):
    """Test user relations."""
    payload = json.dumps({
        'name': 'Test Group with Users',
        'users': users
    })
    response = client.post(
        '/group', data=payload, content_type='application/json'
    )
    assert response.status == '201 Created'

    body = json.loads(response.data.decode())
    parsed_url = urlparse(body['uri'])
    path = parsed_url.path

    group_response = client.get(path, content_type='application/json')
    body = json.loads(group_response.data.decode())
    assert group_response.status == '200 OK'
    assert body['users'] == users
