#!/usr/bin/env python
# -*- coding: utf-8 -*-

from falcon import (
    HTTP_CREATED,
    HTTP_NO_CONTENT,
    HTTPBadRequest,
    HTTPNotFound,
)
from marshmallow import ValidationError

from falcon_experiment.models import (
    Group,
    GroupSchema,
    User,
    UserSchema,
)


class GroupCollection(object):

    # def on_get(self, request, response):
    #     response.document = db.all()

    def on_post(self, request, response):
        schema = GroupSchema()
        try:
            result = schema.load(request.document)
        except ValidationError as error:
            raise HTTPBadRequest(
                'Invalid document submitted',
                error.messages,
            )

        group = result.data
        group.save()
        response.document = {
            'uri': 'http://localhost:8000/group/{}'.format(group.object_key)
        }
        response.status = HTTP_CREATED


class GroupDetail(object):

    def on_get(self, request, response, key):
        schema = GroupSchema()
        try:
            group = Group.get(key)
        except KeyError:
            raise HTTPNotFound
        else:
            response.document = schema.dump(group).data

    def on_delete(self, request, response, key):
        try:
            Group.delete(key)
        except KeyError:
            raise HTTPNotFound
        else:
            response.status = HTTP_NO_CONTENT


class UserCollection(object):

    # def on_get(self, request, response):
    #     response.document = db.all()

    def on_post(self, request, response):
        schema = UserSchema()
        try:
            result = schema.load(request.document)
        except ValidationError as error:
            raise HTTPBadRequest(
                'Invalid document submitted',
                error.messages,
            )

        user = result.data
        user.save()
        response.document = {
            'uri': 'http://localhost:8000/user/{}'.format(user.object_key)
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
