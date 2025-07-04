import http.server
import socketserver
import os

PORT = 8000
STATIC_DIR = "static"

class Handler(http.server.SimpleHTTPRequestHandler):
    pass

if __name__ == "__main__":
    os.chdir(STATIC_DIR)
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()
