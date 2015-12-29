# -*- coding: utf-8 -*-
"""Configuration for SQLAlchemy."""

from sqlalchemy import create_engine, event
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.exc import NoResultFound


engine = create_engine('sqlite:///:memory:')
session_factory = sessionmaker(bind=engine)
# Create a session registry
Session = scoped_session(session_factory)


# Crazy hacks to make SQLite savepoints work with pysqlite/sqlalchemy.
@event.listens_for(engine, "connect")
def do_connect(dbapi_connection, connection_record):
    """
    Disable pysqlite's emitting of the BEGIN statement entirely.

    Also stops it from emitting COMMIT before any DDL.
    """
    dbapi_connection.isolation_level = None


@event.listens_for(engine, "begin")
def do_begin(conn):
    """Emit our own BEGIN."""
    conn.execute("BEGIN")


def get_one_or_create(model, create_kwargs=None, **kwargs):
    """Race free django-style get or create."""
    session = Session()
    query = session.query(model).filter_by(**kwargs)
    try:
        return query.one()
    except NoResultFound:
        session.begin_nested()
        kwargs.update(create_kwargs or {})
        new = model(**kwargs)
        session.add(new)
        try:
            session.commit()
            return new
        except IntegrityError:
            session.rollback()
            return query.one()
