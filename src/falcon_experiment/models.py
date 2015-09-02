#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

from marshmallow import Schema, fields

from falcon_experiment.db import create, get


class Model(object):

    def __init__(self, **kwargs):
        self.object_key = kwargs.pop('object_key')
        self.created_at = kwargs.pop('created_at', datetime.now())

    @classmethod
    def get(cls, key):
        schema = cls.schema()
        key, data = get(cls.bucket_name, key)

        data.update({'object_key': key})
        user = schema.load(data).data
        return user

    def save(self):
        schema = self.schema()
        result = schema.dump(self)
        data = result.data
        self.object_key = create(self.bucket_name, data)


class BaseSchema(Schema):
    object_key = fields.Str()


class GroupSchema(BaseSchema):
    name = fields.Str()
    created_at = fields.DateTime()

    def make_object(self, data):
        return Group(**data)


class UserSchema(BaseSchema):
    name = fields.Str()
    email = fields.Email()
    created_at = fields.DateTime()

    def make_object(self, data):
        return User(**data)


class Group(Model):

    bucket_name = 'group'
    schema = GroupSchema

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = kwargs.pop('name')
        self.created_at = kwargs.pop('created_at', datetime.now())

    def __repr__(self):
        return '<User(name={self.name!r})>'.format(self=self)


class User(Model):

    bucket_name = 'group'
    schema = UserSchema

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = kwargs.pop('name')
        self.email = kwargs.pop('email')

    def __repr__(self):
        return '<User(name={self.name!r})>'.format(self=self)
