from http.server import SimpleHTTPRequestHandler, HTTPServer
from endpoint.endpoint_handler import SendToCorrectEndpointsGet


class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
         SendToCorrectEndpointsGet(self)
    def do_POST(self):
        # TODO: this is still needed to get removed and replaced by the created standart above
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')

        print(f"Received form data: {post_data}")
        file_path = '/postRespose.html'
        if self.path == '/SendToTerminal':
            self.path = file_path
        return SimpleHTTPRequestHandler.do_GET(self)

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