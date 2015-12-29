# -*- coding: utf-8 -*-
"""Schemas for API endpoints, implemented using Marshmallow."""
from marshmallow import Schema, fields, post_load

from falcon_experiment.db import get_one_or_create
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
    users = fields.Nested(
        'UserSchema', many=True, exclude=['created', 'username']
    )

    @post_load
    def make_object(self, data):
        """After validating incoming data will output an object."""
        name = data['name']
        return get_one_or_create(Group, name=name, create_kwargs=data)


class UserSchema(BaseSchema):

    """Schema to de/serialise the User model."""

    email = fields.Email(required=True)
    username = fields.Str(required=True)

    @post_load
    def make_object(self, data):
        """After validating incoming data will output an object."""
        email = data['email']
        return get_one_or_create(User, email=email, create_kwargs=data)
