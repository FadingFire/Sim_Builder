from python.src.main.endpoint.post_endpoints.command_line import handle_command
from python.src.main.endpoint.get_endpoints.command_input import command_input_page
from python.src.main.endpoint.error_endpoints.page_not_found import HandlePageNotFound

def send_to_correct_endpoints(self):
    """runs the correct function to the corresponding url"""
    match self.path:
        case '/commandline':
            handle_command(self)
        case '/':
            command_input_page(self)
        case _:
            HandlePageNotFound(self)
        