#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Configuration for SQLAlchemy."""

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('sqlite:///:memory:')
session_factory = sessionmaker(bind=engine)
# Create a session registry
Session = scoped_session(session_factory)
