#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Schemas for API endpoints, implemented using Marshmallow."""
from marshmallow import Schema, fields, post_load

from falcon_experiment.models import (
    Group,
    User,
)


class BaseSchema(Schema):

    """Base Schema class for DRY enforcement of resource attributes."""

    created = fields.DateTime(dump_only=True)

    class Meta(object):
        strict = True


class GroupSchema(BaseSchema):

    """Schema to de/serialise the Group model."""

    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    users = fields.List(fields.Url(relative=True))

    @post_load
    def make_object(self, data):
        """After validating incoming data will output an object."""
        return Group(**data)


class UserSchema(BaseSchema):

    """Schema to de/serialise the User model."""

    email = fields.Email(required=True)
    username = fields.Str(required=True)

    @post_load
    def make_object(self, data):
        """After validating incoming data will output an object."""
        return User(**data)
