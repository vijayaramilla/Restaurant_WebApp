# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 19:55:05 2017

@author: Santhosh
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

#Create a sqlalchemy session maker object
DBSession = sessionmaker(bind= engine)
#Create Session and add your sql queries to session
session = DBSession()

#Class to handle all http requests
class webserverHandler(BaseHTTPRequestHandler):
    #method to handle get request
    def do_GET(self):
        try:
            if self.path.endswith("delete"):
                #grab the id
                restaurantId = self.path.split("/")[2]
                restaurantQuery = session.query(Restaurant).filter_by(
                        id = restaurantId).one()
                
                if restaurantQuery: 
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h1>"
                    output += "Are you sure you want to delete %s" % restaurantQuery.name
                    output += "</h1>"
                    output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/%s/delete'>" % restaurantId
                    #output += "<input name = 'newRestaurantName' type='text' placeholder = '%s' >" % restaurantQuery.name
                    output += "<input type='submit' value='Delete'>"
                    output += "</form></body></html>"
                    self.wfile.write(bytes(output, "utf-8"))
                    print(output)
                    
            if self.path.endswith("edit"):
                #grab the id
                restaurantId = self.path.split("/")[2]
                restaurantQuery = session.query(Restaurant).filter_by(
                        id = restaurantId).one()
                
                if restaurantQuery: 
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h1>"
                    output += "restaurantQuery.name"
                    output += "</h1>"
                    output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/%s/edit'>" % restaurantId
                    output += "<input name = 'newRestaurantName' type='text' placeholder = '%s' >" % restaurantQuery.name
                    output += "<input type='submit' value='Rename'>"
                    output += "</form></body></html>"
                    self.wfile.write(bytes(output, "utf-8"))
                    print(output)
                
            
            if self.path.endswith("/restaurants/new"):
                #create the response
                #set the response code.
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/new'>"
                output += "<input name = 'newRestaurantName' type = 'text' placeholder = 'New Restaurant Name' > "
                output += "<input type='submit' value='Create'>"
                output += "</form></body></html>"
                self.wfile.write(bytes(output, "utf-8"))
                print(output)
                return
                            
            if self.path.endswith("/Restaurants"):
                #create the response
                #set the response code.
                rest_list = session.query(Restaurant).all()
                msg = ""
                msg += "<a href = '/restaurants/new' > Make a New Restaurant Here </a></br></br>"
                
                self.send_response(200)
                #send header
                self.send_header('Content-type','text/html')
                self.end_headers()
                
                msg += "<htlm><body>"
                for rest in rest_list:
                    msg += rest.name
                    msg += "</br>"
                    msg += "<a href = '/restaurants/%s/edit' > Edit</a>" % rest.id
                    msg +=  "</br>"
                    msg += "<a href = '/restaurants/%s/delete' > Delete</a>" % rest.id
                    msg +=  "</br>"
                
                msg += "</htlm></body>"
                self.wfile.write(bytes(msg, "utf-8"))
                print(msg)
                return

        except IOError:
            self.send_error(404, "file not found %s" % self.path)

    def do_POST(self):
        #setup the headers
        try:
            
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.get('content-type'))
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')

                    # Create new Restaurant Object
                    newRestaurant = Restaurant(name=messagecontent[0].decode("utf-8"))
                    session.add(newRestaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/Restaurants')
                    self.end_headers()
            
            if self.path.endswith("edit"):
                ctype, pdict = cgi.parse_header(
                        self.headers.get('content-type'))
                
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    restaurantIDPath = self.path.split("/")[2]
                    myRestaurantQuery = session.query(Restaurant).filter_by(
                        id=restaurantIDPath).one()
                    
                    if myRestaurantQuery != []:
                        myRestaurantQuery.name = messagecontent[0].decode("utf-8")
                        session.add(myRestaurantQuery)
                        session.commit()

                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/Restaurants')
                        self.end_headers()
            
            if self.path.endswith("delete"):
                ctype, pdict = cgi.parse_header(
                        self.headers.get('content-type'))
            
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(
                        id=restaurantIDPath).one()
                    
                if myRestaurantQuery != []:
                    session.delete(myRestaurantQuery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/Restaurants')
                    self.end_headers()
                    
            
        except Exception as inst:
            print(inst)



def main():
    try:
        #define the port number
        port = 8080
        # setup the server
        server = HTTPServer(('',port), webserverHandler)
        print ("Web Server running on port %s" % port)
        #keep running the server until user interrupt
        server.serve_forever()
    except KeyboardInterrupt:
        print ("^C entered, stopping webserver...")
        server.socket.close()
if __name__ == '__main__':
    main()