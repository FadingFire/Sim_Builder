from http.server import SimpleHTTPRequestHandler
from model.paths import command_input_page

def command_input_page(self):
    self.path = command_input_page()
    return SimpleHTTPRequestHandler.do_GET(self)