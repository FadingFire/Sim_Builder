from http.server import SimpleHTTPRequestHandler
from python.src.main.model.paths import get_page_path


def handle_command(self):
    """the main order of when what function happens"""
    command = parse_command(self)
    if command[0] != 200:
        return 505
    use_command(command[1])
    self.path = get_page_path("postRespose")
    return SimpleHTTPRequestHandler.do_GET(self)


def parse_command(self):
    """this parses the POST data to separate the input name from its value"""
    content_length = int(self.headers['Content-Length'])
    post_data = self.rfile.read(content_length).decode('utf-8')
    validate_data = validata_raw_post_data(post_data)
    if validate_data[0] != 200:
        return 505
    command = post_data[validate_data[1]:len(post_data)]
    print(command)
    if validate_command(self, command) != 200:
        return 505
    return 200, command


def validata_raw_post_data(post_data):
    """validates the post data to check if there is a value"""
    for i, char in enumerate(post_data):
        if char == "=" and i+1 <= len(post_data):
            return 200, i+1
    return 404, 0


def validate_command(self, command):
    """
    check against all the possible commands that you can have in blueksy to check if it does exist.
    run the command in a dummy blueksy terminal to see the response?
    """
    return 200


def use_command(command):
    """
    runs the command using a the bluesky plugin.
    this will only run live and should maybe not be used to stop or start blueksy?
    """
    print(command)
    return
