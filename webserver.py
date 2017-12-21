#from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from http.server import BaseHTTPRequestHandler, HTTPServer

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
                self.wfile.write(bytes(msg, "utf-8"))
                print(msg)
                return
        except IOError:
            self.send_error(404, "file not found %s" % self.path)
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
