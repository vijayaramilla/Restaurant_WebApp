#import Flask class from flask library
from flask import Flask, render_template

"""
1. create an instance of Flask class with the running application as argument
2. Any time a program is run in python __name__ variable is defined for the application.
3. The application that is run by python interpretor gets the __name__ variable set to 
'__main__'. where as all other imported python files get the __name__ variable set to actual
file name.
"""
app = Flask(__name__)


#To support CRUD operations imports necessary libraries.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


#Create the SQLAlchemy engine
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
"""
use decorators to wrap the function inside the functions that flask has created.
Here the function helloWorld is wrapped inside route() function of flask.

So calling either of below routes (/ or /hello) the helloWorld function gets executed.
"""
@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    #create a database query to list all restaurants.
    restaurant = session.query(Restaurant).filter_by(id = 
                              restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    return render_template('menu.html', restaurant = restaurant, 
                           items = items)
    """
    output = ''
    output += '<h1>'
    output += restaurant.name
    output += '</h1>'
    for item in items:
        output += item.name
        output += '</br>'
        output += item.price
        output += '</br>'
        output += item.description
        output += '</br></br>'
    """

# Task 1: Create route for newMenuItem function here

@app.route('/restaurant/<int:restaurant_id>/new')
def newMenuItem(restaurant_id):
    return "page to create a new menu item. Task 1 complete!"

# Task 2: Create route for editMenuItem function here

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit')
def editMenuItem(restaurant_id, menu_id):
    return "page to edit a menu item. Task 2 complete!"

# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
    return "page to delete a menu item. Task 3 complete!"

"""
this if statement makes sure that the program local server is only created
if the program is executed directly from the python interpreter and not used 
as an imported module. By default the server is accessible from the host machine
and not from any other computer
"""
if __name__ == '__main__':
    # app.debug will reload the server each time a change is made in the code.
    #no need to restart the server each time u make a change.
    #this also provides a debugger in the browser.
    app.debug = True
    #run the local server with our application.
    # host = '0.0.0.0' tells the server to listen on all public machines.
    app.run(host = '0.0.0.0', port = 5000)

