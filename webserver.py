import simpleNetworkScanner as sns
from http.server import BaseHTTPRequestHandler, HTTPServer

hostName = sns.getIpAdresses()[1][:-3]
serverPort = 80

def getHtml():
    with open('website.html', 'r') as handle:
        lines = handle.readlines()
    return lines

def checkHomeFiles():
    with open('max.bool', 'r') as handle:
        maxOnline = bool(handle.readline())
    with open('alex.bool', 'r') as handle:
        alexOnline = bool(handle.readline())
    return maxOnline, alexOnline
        

class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        maxOnline, alexOnline = checkHomeFiles()
        htmlFile = getHtml()
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        if maxOnline:
            self.wfile.write(bytes('<p id="title" Maexchen ist Home</p>', 'utf-8'))
        if alexOnline:
            self.wfile.write(bytes('<p id="title">Alex ist Home</p>', 'utf-8'))
        for line in htmlFile:
            self.wfile.write(bytes(line, 'utf-8'))
        '''
        self.wfile.write(bytes('<html><head><title>Who is home?</title></head>', 'utf-8'))
        self.wfile.write(bytes('<body>','utf-8'))
        self.wfile.write(bytes(f'<p>{whoIsHome}</p>','utf-8'))
        self.wfile.write(bytes('</body></html>','utf-8'))
        '''


if __name__ == '__main__':
    print(f'Serving at {hostName}:{serverPort}')
    webServer = HTTPServer((hostName, serverPort), MyServer)

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
