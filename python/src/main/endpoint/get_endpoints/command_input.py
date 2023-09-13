from http.server import SimpleHTTPRequestHandler

from python.src.main.model.paths import command_input_page_path

def command_input_page(self):
    self.path = command_input_page()
    return SimpleHTTPRequestHandler.do_GET(self)
