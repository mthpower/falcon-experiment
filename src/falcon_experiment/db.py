# -*- coding: utf-8 -*-
"""Configuration for SQLAlchemy."""

from sqlalchemy import create_engine, event
from sqlalchemy.orm import scoped_session, sessionmaker


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
