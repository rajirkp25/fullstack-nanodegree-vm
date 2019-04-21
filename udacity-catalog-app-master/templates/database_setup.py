from sqlalchemy import Column, ForeignKey, Integer, String, UnicodeText
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from pip._vendor.urllib3.contrib._securetransport.bindings import Boolean
import datetime
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    avatar = Column(String(250))
    active = Column(Boolean, default=False)
    tokens = Column(String(250))
    created_at = Column(datetime, default=datetime.datetime.utcnow())


# book category
class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(UnicodeText(10000))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }


# book name
class CategoryItem(Base):
    __tablename__ = 'category_item'
    i = 0
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(UnicodeText(10000), nullable=False)
    price = Column(String(8))
    author = Column(String(250), nullable=False)
    best_seller_rank = Column(Integer, default=i)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    # added by user
    user_id = Column(Integer, ForeignKey('user.id'))  
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'course': self.category_id,
        }


engine = create_engine('sqlite:///bookcats.db')

Base.metadata.create_all(engine)