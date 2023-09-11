from http.server import SimpleHTTPRequestHandler, HTTPServer
from endpoint.endpoint_handler import SendToCorrectEndpointsGet


class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        SendToCorrectEndpointsGet(self)
    def do_POST(self):
        SendToCorrectEndpointsGet(self)

def run(server_class=HTTPServer, handler_class=CustomHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()
    if KeyboardInterrupt:
        httpd.server_close()
        exit()

if __name__ == "__main__":
        run()