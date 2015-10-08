#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Models are defined here using SQLAlchemy."""

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Model = declarative_base()


class Group(Model):

    """A Group is a container for users."""

    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now())
    name = Column(String)

    def __str__(self):
        """Return a human-readable representation of the object."""
        return '<Group(name="{name}")>'.format(
            name=self.name,
        )


class User(Model):

    """A basic User.

    The email address is the primary key. We will use OIDC for auth'n.
    """

    __tablename__ = 'users'

    email = Column(String, primary_key=True)
    created = Column(DateTime, default=datetime.now())
    username = Column(String)

    def __repr__(self):
        """Return a human-readable representation of the object."""
        return '<User(email="{email}")>'.format(
            email=self.email,
        )
