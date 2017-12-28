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
            if self.path.endswith("/restaurants/new"):
                #create the response
                #set the response code.
                self.send_response(200)
                #send header
                self.send_header('Content-type','text/html')
                self.end_headers()

                #construct actual output
                msg = ""
                msg += "<html><body>"
                msg += "<h1>Make a new Restaurant</h1>"
                msg += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
                msg += "<input name='newRestaurantName' type='text' placeholder = 'New Restaurant Name'>"
                msg += "<input type='submit' value='Create'>"
                msg += "</form></body></html>"
                self.wfile.write(bytes(msg, "utf-8"))
                print(msg)
                return
            if self.path.endswith("/restaurants"):
                #create the response
                #set the response code.
                self.send_response(200)
                #send header
                self.send_header('Content-type','text/html')
                self.end_headers()
                
                #Get the list of restaraunts
                rest_list = session.query(Restaurant).all()
                
                #construct actual output
                msg = ""
                msg += "<htlm><body>"
                msg += "<a href = '/restaurants/new' > Make a New Restaurant Here</a></br></br>"
                #msg += '''<form method='POST' enctype='multipart/form-data' action='/new'><h2>?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                for rest in rest_list:
                    msg += rest.name
                    msg += "</br>"
                    msg += "<a href = '#' > Edit</a>"
                    msg +=  "</br>"
                    msg += "<a href = '#' > Delete</a>"
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
                ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
                print("enter loop")
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                
                    #create a new restraunt in database
                    newRestaurant = Restaurant(name=messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()
                    
                    self.send_response(301)
                    self.send_header('Content-type','text/html')
                    self.send_header('Location', '/restaurants')
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
