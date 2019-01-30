#!/usr/bin/env python

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Brand(Base):
    __tablename__ = 'brand'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }


class Snowboard(Base):
    __tablename__ = 'snowboard'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    style = Column(String(250))
    brand_id = Column(Integer, ForeignKey('brand.id'))
    brand = relationship(Brand)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

# We added this serialize function to be able to send JSON objects
# in a serializable format
    @property
    def serialize(self):

        return {
           'name': self.name,
           'style': self.style,
           'id': self.id,
        }

engine = create_engine('sqlite:///brandsnowboard.db')

Base.metadata.create_all(engine)
