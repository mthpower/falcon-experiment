#!/usr/bin/env python
# -*- coding: utf-8 -*-
from marshmallow import Schema, fields, post_load

from falcon_experiment.models import (
    Group,
    User,
)


class BaseSchema(Schema):
    created = fields.DateTime(dump_only=True)

    class Meta(object):
        strict = True


class GroupSchema(BaseSchema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    users = fields.List(fields.Url(relative=True))

    @post_load
    def make_object(self, data):
        return Group(**data)


class UserSchema(BaseSchema):
    email = fields.Email(required=True)
    username = fields.Str(required=True)

    @post_load
    def make_object(self, data):
        return User(**data)
