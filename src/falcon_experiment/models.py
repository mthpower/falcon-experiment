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
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.exc import NoResultFound

from falcon_experiment.db import Session


class QueryMixin(object):

    """Mixin for common query patterns."""

    @classmethod
    def get_one_or_create(cls, create_kwargs=None, **kwargs):
        """Race free django-style get or create."""
        query = Session.query(cls).filter_by(**kwargs)
        try:
            return query.one()
        except NoResultFound:
            Session.begin_nested()
            kwargs.update(create_kwargs or {})
            new = cls(**kwargs)
            Session.add(new)
            try:
                Session.commit()
                return new
            except IntegrityError:
                Session.rollback()
                return query.one()


Model = declarative_base(cls=QueryMixin)

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
