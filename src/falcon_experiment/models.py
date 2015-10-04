#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Model = declarative_base()


class Group(Model):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now())
    name = Column(String)

    def __repr__(self):
        return '<Group(name="{name}")>'.format(
            name=self.name,
        )


class User(Model):
    __tablename__ = 'users'

    email = Column(String, primary_key=True)
    created = Column(DateTime, default=datetime.now())
    username = Column(String)

    def __repr__(self):
        return '<User(email="{email}")>'.format(
            email=self.email,
        )
