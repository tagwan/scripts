from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sys
import locale

data = {'result': 'this is a test'}
host = ('localhost', 8080)


class WebServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())


if __name__ == '__main__':
    addr = len(sys.argv) < 2 and "localhost" or sys.argv[1]
    port = len(sys.argv) < 3 and 8080 or locale.atoi(sys.argv[2])
    server = HTTPServer(host, WebServer)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()