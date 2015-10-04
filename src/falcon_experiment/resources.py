#!/usr/bin/env python
# -*- coding: utf-8 -*-
from falcon import (
    HTTP_CREATED,
    HTTP_NO_CONTENT,
    HTTPBadRequest,
    HTTPNotFound,
)
from marshmallow import ValidationError

from falcon_experiment.db import Session
from falcon_experiment.models import (
    Group,
    User,
)
from falcon_experiment.schemas import (
    GroupSchema,
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
        Session.add(group)
        # Commit early to return the id in the uri
        Session.commit()
        response.document = {
            'uri': 'http://localhost:8000/group/{}'.format(group.id)
        }
        response.status = HTTP_CREATED


class GroupDetail(object):

    def on_get(self, request, response, id):
        schema = GroupSchema()
        group = Session.query(Group).get(id)
        if group is None:
            raise HTTPNotFound

        response.document = schema.dump(group).data

    def on_delete(self, request, response, id):
        group = Session.query(Group).get(id)
        if group is None:
            raise HTTPNotFound

        Session.delete(group)
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
        Session.add(user)
        # Commit early to return the id in the uri
        Session.commit()
        response.document = {
            'uri': 'http://localhost:8000/user/{}'.format(user.email)
        }
        response.status = HTTP_CREATED


class UserDetail(object):

    def on_get(self, request, response, email):
        schema = UserSchema()
        user = Session.query(User).get(email)
        if user is None:
            raise HTTPNotFound

        response.document = schema.dump(user).data

    def on_delete(self, request, response, email):
        user = Session.query(User).get(email)
        if user is None:
            raise HTTPNotFound

        Session.delete(user)
        response.status = HTTP_NO_CONTENT
