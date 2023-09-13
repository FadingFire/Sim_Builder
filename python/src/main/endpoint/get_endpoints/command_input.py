from http.server import SimpleHTTPRequestHandler
from python.src.main.model.paths import get_page_path

def command_input_page(self):
    self.path = get_page_path("commandInputPage")
    print(self.path)
    return SimpleHTTPRequestHandler.do_GET(self)
