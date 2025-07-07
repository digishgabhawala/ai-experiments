import http.server
import socketserver
import os

PORT = 8000
STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC_DIR, **kwargs)

def run_server(server_class=socketserver.TCPServer, handler_class=Handler, port=PORT):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Serving at port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    # To run the server directly
    os.chdir(STATIC_DIR)
    run_server()
