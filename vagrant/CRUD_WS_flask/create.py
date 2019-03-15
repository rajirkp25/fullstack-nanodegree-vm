from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

session = DBSession()
myfirstRestaurant = Restaurant(name="Pizza Place")

session.add(myfirstRestaurant)
session.commit()

menuItem1 = MenuItem(name="Veggie Pizza", description="Veg Pizza with Spinach, Onion, Olive, Jalapeneos and pineapples",
                     price="$7.50", course="Entree", restaurant=myfirstRestaurant)

session.add(menuItem1)
session.commit()
