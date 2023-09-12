from http.server import SimpleHTTPRequestHandler, HTTPServer
from endpoint.endpoint_handler import send_to_correct_endpoints


class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        send_to_correct_endpoints(self)
    def do_POST(self):
        send_to_correct_endpoints(self)

def run(server_class=HTTPServer, handler_class=CustomHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()
    if KeyboardInterrupt:
        httpd.server_close()
        exit()
