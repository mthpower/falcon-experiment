#!/usr/bin/env python
# -*- coding: utf-8 -*-

from falcon import (
    HTTP_CREATED,
    HTTP_NO_CONTENT,
    HTTPBadRequest,
    HTTPNotFound,
)

from falcon_experiment.models import User, UserSchema


class UserCollection(object):

    # def on_get(self, request, response):
    #     response.document = db.all()

    def on_post(self, request, response):
        schema = UserSchema()
        result = schema.load(request.document)
        if result.errors:
            raise HTTPBadRequest(
                'Invalid document submitted',
                result.errors,
            )

        user = result.data
        user.save()
        response.document = {
            'uri': 'http://localhost:8000/users/{}'.format(user.object_key)
        }
        response.status = HTTP_CREATED


class UserDetail(object):

    def on_get(self, request, response, key):
        schema = UserSchema()
        try:
            user = User.get(key)
        except KeyError:
            raise HTTPNotFound
        else:
            response.document = schema.dump(user).data

    def on_delete(self, request, response, key):
        try:
            User.delete(key)
        except KeyError:
            raise HTTPNotFound
        else:
            response.status = HTTP_NO_CONTENT
