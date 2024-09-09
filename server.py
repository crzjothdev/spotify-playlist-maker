# basic http server running on a different thread
# used to catch the authorization code the
# Spotify API send when call our callback funtion
from http.server import BaseHTTPRequestHandler, HTTPServer
from shared import auth_queue

class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Authentication successful. You can close this window.')

        auth_code = self.path.split('code=')[-1]
        auth_queue.put(auth_code)

def run_server():
    # if current program isn't running on a docker container
    # change 0.0.0.0 to 127.0.0.1 also the port number if necessary
    server_address = ('0.0.0.0', 8889)
    httpd = HTTPServer(server_address, OAuthHandler)
    httpd.serve_forever()

        