from sqlalchemy import Column, ForeignKey, Integer, String, UnicodeText, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from datetime import datetime
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    avatar = Column(String(250))
    active = Column(Boolean, default=False)
    tokens = Column(String(250))
    created_at = Column(DateTime(), default=datetime.utcnow())

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.user_id,
            'name': self.name,
            'email':self.email,
            'avatar':self.avatar,
            'tokens':self.tokens
        }


# book category
class Category(Base):
    __tablename__ = 'category'

    cat_id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(UnicodeText(10000))
    tile = Column(String(250))
        # added by user
    user_id = Column(Integer, ForeignKey('user.user_id'))  
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.cat_id,
            'tile':self.tile
        }


# book name
class CategoryItem(Base):
    __tablename__ = 'category_item'
    i = 0
    item_id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(UnicodeText(10000), nullable=False)
    price = Column(String(8))
    author = Column(String(250), nullable=False)
    best_seller_rank = Column(Integer, default=i)
    cat_id = Column(Integer, ForeignKey('category.cat_id'))
    category = relationship(Category)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'id': self.item_id,
            'price': self.price,
            'cat_id': self.cat_id,
        }


engine = create_engine('sqlite:///bookcats.db')

Base.metadata.create_all(engine)