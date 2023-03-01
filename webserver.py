import simpleNetworkScanner as sns
from http.server import BaseHTTPRequestHandler, HTTPServer

hostName = sns.getIpAdresses()[1][:-3]
serverPort = 80
insertLine = 45

darkClass = '<div class="darkClass"><p class="notHome">Nicht zu Hause</p></div>'

def getHtml():
    with open('website.html', 'r') as handle:
        lines = handle.readlines()
    return lines

def checkHomeFiles():
    with open('max.bool', 'r') as handle:
        maxOnline = handle.readline().startswith('True')
    with open('alex.bool', 'r') as handle:
        alexOnline = handle.readline().startswith('True')
    return maxOnline, alexOnline
        

class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        maxOnline, alexOnline = checkHomeFiles()
        htmlFile = getHtml()
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        for index, line in enumerate(htmlFile):

            if line.startswith('<!--Add darkClass, Max-->'):
                if not maxOnline:
                    print('maexchen offline')
                    self.wfile.write(bytes(darkClass, 'utf-8'))
                continue
            elif line.startswith('<!--Add darkClass, Alex-->'):
                if not alexOnline:
                    self.wfile.write(bytes(darkClass, 'utf-8'))
                continue

            self.wfile.write(bytes(line, 'utf-8'))


if __name__ == '__main__':
    print(f'Serving at {hostName}:{serverPort}')
    webServer = HTTPServer((hostName, serverPort), MyServer)

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
