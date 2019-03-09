# #!/usr/bin/env python3
# Database setup code for catalog

import sys
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship
from pip._vendor.pyparsing import nullDebugAction
from msilib import type_nullable

Base = declarative_base()


class Restaurant(Base):
    __tablename__ = 'restaurant'
    name = Column(String(80))
    id = Column(Integer, primary_key=True)


class MenuItem(Base):
    __tablename__ = 'menuitem'
    name = Column(String(80))
    id = Column(Integer, primary_key=True)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)


engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.create_all(engine)
