'''
This script defines a webserver that serves a simple HTML page
showing wehter Alex or Maexchen were logged into the home wifi
within the last 5 minutes
'''
import simpleNetworkScanner as sns
from http.server import BaseHTTPRequestHandler, HTTPServer

# Get own IP address via simpleNetworkScanner method to use as IP for the 
# Webserver
hostName = sns.getIpAdresses()[1][:-3]
# Port of the webserver
serverPort = 80

# This line of html is inserted into the webpage to gray out namecard of 
# Alex or Maexchen if they are not at home
darkClass = '<div class="darkClass"><p class="notHome">Nicht zu Hause</p></div>'

# open the htmp file and return it as a list of lines
def getHtml():
    with open('website.html', 'r') as handle:
        lines = handle.readlines()
    return lines

# check for savefiles which contain wether the specified person is logged
# as at home or not
#
# returns: a tuple of booleans each True if the person is at home, False if not
def checkHomeFiles():
    with open('max.bool', 'r') as handle:
        maxOnline = handle.readline().startswith('True')
    with open('alex.bool', 'r') as handle:
        alexOnline = handle.readline().startswith('True')
    return maxOnline, alexOnline
        
# Class defines a webserver that serves a simple HTML page and manipulates the
# base webpage to show wehter Alex or Maexchen are logged into the home wifi
class MyServer(BaseHTTPRequestHandler):

    # This method is called when a GET request is made to the server by a client
    def do_GET(self):
        # Calls the function above to check who is home
        maxOnline, alexOnline = checkHomeFiles()
        # Call the function to get the html file
        htmlFile = getHtml()
        # Send a 'OK' response to the client
        self.send_response(200)
        # Send the Header of the server response
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        # Iteraates over the lines of the html file, inserting the darkClass line
        # if the person is not at home
        for index, line in enumerate(htmlFile):
            # Check for Maexchen
            if line.startswith('<!--Add darkClass, Max-->'):
                if not maxOnline:
                    # Insert the darkClass line instead of the comment line
                    self.wfile.write(bytes(darkClass, 'utf-8'))
                continue
            # Also check for Alex
            elif line.startswith('<!--Add darkClass, Alex-->'):
                if not alexOnline:
                    # Insert the darkClass line instead of the comment line
                    self.wfile.write(bytes(darkClass, 'utf-8'))
                continue

            self.wfile.write(bytes(line, 'utf-8'))

# Execute this if the script is called directly
if __name__ == '__main__':
    # Short console output
    print(f'Serving at {hostName}:{serverPort}')
    # Create the webserver
    webServer = HTTPServer((hostName, serverPort), MyServer)
    # Serve until console interrupt happens
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    # close the webserver
    webServer.server_close()
