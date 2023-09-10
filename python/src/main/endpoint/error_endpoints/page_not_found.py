from http.server import SimpleHTTPRequestHandler
from model.paths import page_not_found_path

def HandlePageNotFound(self):
    self.path = page_not_found_path()
    return SimpleHTTPRequestHandler.do_GET(self)