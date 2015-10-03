#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

from marshmallow import Schema, fields

from falcon_experiment.db import create, delete, get


class Model(object):

    primary_key = 'object_key'

    def __init__(self, **kwargs):
        self.object_key = kwargs.get('object_key')
        self.created_at = kwargs.get('created_at', datetime.now())

    @classmethod
    def get(cls, key):
        schema = cls.schema()
        key, data = get(cls.bucket_name, key)
        model = schema.load(data).data
        return model

    @classmethod
    def delete(cls, key):
        delete(cls.bucket_name, key)

    def save(self):
        schema = self.schema()
        result = schema.dump(self)
        data = result.data
        key = getattr(self, self.primary_key)
        self.object_key = create(self.bucket_name, data, key)


class BaseSchema(Schema):
    object_key = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

    class Meta(object):
        strict = True


class GroupSchema(BaseSchema):
    name = fields.Str(required=True)
    users = fields.List(fields.Url(relative=True))

    def make_object(self, data):
        import ipdb; ipdb.set_trace()
        return Group(**data)


class UserSchema(BaseSchema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)

    def make_object(self, data):
        return User(**data)


class Group(Model):

    bucket_name = 'group'
    schema = GroupSchema

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = kwargs.get('name')
        self.users = kwargs.get('users')

    def __repr__(self):
        return '<User(name={self.name!r})>'.format(self=self)


class User(Model):

    bucket_name = 'group'
    schema = UserSchema
    primary_key = 'email'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = kwargs.get('name')
        self.email = kwargs.get('email')

    def __repr__(self):
        return '<User(name={self.name!r})>'.format(self=self)
