#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from falcon import (
    API,
    HTTP_CREATED,
    HTTPNotAcceptable,
    HTTPNotFound,
    HTTPUnsupportedMediaType,
)
from marshmallow import Schema, fields


class Storage(object):
    _db = {}

    def get(self, key):
        return self._db[key]

    def set(self, key, value):
        self._db[key] = value

    def delete(self, key):
        del self._db[key]

    def clear(self):
        self._db = {}

    def all(self):
        return self._db


class UserSchema(Schema):
    name = fields.Str()
    email = fields.Email()
    created_at = fields.DateTime()


class UserCollection(object):

    def on_get(self, request, response):
        response.data = json.dumps(db.all())

    def on_post(self, request, response):
        response.body = 'Collection Endpoint'
        response.status = HTTP_CREATED


class UserDetail(object):

    def on_get(self, request, response, username):
        try:
            response.data = json.dumps(db.get(username))
        except KeyError:
            raise HTTPNotFound()

    def on_post(self, request, response, username):
        response.body = 'Detail Endpoint'
        response.status = HTTP_CREATED


class RequireJSON(object):

    def process_request(self, req, resp):
        if not req.client_accepts_json:
            raise HTTPNotAcceptable(
                'This API only supports responses encoded as JSON.',
            )

        if req.method in ('POST', 'PUT', 'PATCH'):
            if 'application/json' not in req.content_type:
                raise HTTPUnsupportedMediaType(
                    'This API only supports requests encoded as JSON.',
                )


db = Storage()
db.set(
    'Alice', {
        'name': 'Alice',
        'email': 'alice@example.com',
        'created_at': 'time'
    }
)
db.set(
    'Bob', {
        'name': 'Bob',
        'email': 'bob@example.com',
        'created_at': 'time'
    }
)

api = application = API(
    middleware=[
        RequireJSON(),
    ]
)
api.add_route('/users', UserCollection())
api.add_route('/users/{username}', UserDetail())

if __name__ == '__main__':
    # For debugging and development
    from werkzeug.serving import run_simple
    run_simple(
        hostname='localhost',
        port=8080,
        application=application,
        use_reloader=True,
    )
