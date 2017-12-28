from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

#Create a sqlalchemy session maker object
DBSession = sessionmaker(bind= engine)
#Create Session and add your sql queries to session
session = DBSession()

#this is the staging zone. All changes here need to be committed later.

"""
make an entry into database: this is similar to making an object in python.

example: 
    newEntry = ClassName(property="Value", ..)
    session.add(newEntry)
    session.commit()
"""

myFirstRestaurant = Restaurant(name= "Pizza Hut")
session.add(myFirstRestaurant)
session.commit()

seconf_rest = Restaurant(name= "Subway")
session.add(seconf_rest)
session.commit()

third = Restaurant(name= "Dominos")
session.add(third)
session.commit()

fourth = Restaurant(name= "Wendy's")
session.add(fourth)
session.commit()

#check if the entry is added
print(session.query(Restaurant).all())

#Now lets add entru to menuItem database
cheese_pizza = MenuItem(name ="Cheese pizza", 
        description="too much cheese",
        course="Entree", 
        price= "$8.99", 
        restaurant=myFirstRestaurant)

pasta = MenuItem(name ="Parmesa Pasta", 
        description="pasta",
        course="Entree", 
        price= "$10", 
        restaurant=myFirstRestaurant)

bread = MenuItem(name ="Garlic Bread", 
        description = "Bread",
        course="Starter", 
        price= "$5", 
        restaurant=myFirstRestaurant)
session.add(cheese_pizza)
session.add(pasta)
session.add(bread)
session.commit()
print(session.query(MenuItem).all())
