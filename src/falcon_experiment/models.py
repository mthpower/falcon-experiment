# -*- coding: utf-8 -*-
"""Models are defined here using SQLAlchemy."""

from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Model = declarative_base()

groups_to_users = Table(
    'groups_to_users',
    Model.metadata,
    Column('group_id', Integer, ForeignKey('groups.id')),
    Column('user_email', Integer, ForeignKey('users.email'))
)


class Group(Model):

    """A Group is a container for users."""

    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now())
    name = Column(String, nullable=False)
    users = relationship(
        'User',
        secondary='groups_to_users',
        backref=backref('groups', lazy='dynamic')
    )

    def __repr__(self):
        """Return a human-readable representation of the object."""
        return '<Group(name="{name}")>'.format(
            name=self.name,
        )


class User(Model):

    """
    A basic User.

    The email address is the primary key. We will use OIDC for auth'n.
    """

    __tablename__ = 'users'

    email = Column(String, primary_key=True)
    created = Column(DateTime, default=datetime.now())
    username = Column(String, nullable=False)

    def __repr__(self):
        """Return a human-readable representation of the object."""
        return '<User(email="{email}")>'.format(
            email=self.email,
        )
