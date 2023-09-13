from http.server import SimpleHTTPRequestHandler
from python.src.main.model.paths import get_page_path

def HandlePageNotFound(self):
    self.path = get_page_path('404')
    return SimpleHTTPRequestHandler.do_GET(self)