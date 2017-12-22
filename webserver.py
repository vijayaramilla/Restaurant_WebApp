from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi

#Class to handle all http requests
class webserverHandler(BaseHTTPRequestHandler):
    #method to handle get request
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                #create the response
                #set the response code.
                self.send_response(200)
                #send header
                self.send_header('Content-type','text/html')
                self.end_headers()

                #construct actual output
                msg = ""
                msg += "<html><body>Hello!</body></html>"
                msg += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                self.wfile.write(bytes(msg, "utf-8"))
                print(msg)
                return

            #Add another route
            if self.path.endswith("/hola"):
                #create the response
                #set the response code.
                self.send_response(200)
                #send header
                self.send_header('Content-type','text/html')
                self.end_headers()

                #construct actual output
                msg = ""
                msg += "<html><body>&#161Hola <a href = '/hello' > Back to Hello</a></body></html>"
                msg += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                self.wfile.write(bytes(msg, "utf-8"))
                print(msg)
                return

        except IOError:
            self.send_error(404, "file not found %s" % self.path)

    def do_POST(self):
        #setup the headers
        try:
            self.send_response(301)
            self.send_header('Content-type','text/html')
            self.end_headers()

            #parse the message sent by the client using cgi
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            #check if content-type is of type FORM
            if ctype == 'multipart/form-data':
                #collect all the fields in the form
                fields = cgi.parse_multipart(self.rfile, pdict)
                #assign message in fields to array
                messagecontent = fields.get('message')
    
            msg = ""
            msg += "<html><body>"
            msg += "<h2> Okay, chek this: </h2>"
            msg += "<h1> %s </h1>" % messagecontent[0].decode("utf-8")
            print(msg)
            msg += '''<form method='POST' enctype='multipart/form-data'
                action='/hello'><h2>What would you like me to say?</h2>
                <input name="message" type="text" >
                <input type="submit" value="Submit"> </form>'''

            msg += "</body></html>"

            self.wfile.write(bytes(msg, "utf-8"))
            print (msg)

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
