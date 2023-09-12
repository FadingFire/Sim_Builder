from post_endpoints.command_line import handle_command

from get_endpoints.command_input import CommandInputPage

from error_endpoints.page_not_found import HandlePageNotFound

def send_to_correct_endpoints(self):
    match self.path:
        case '/commandline':
            handle_command(self)
        case '/':
            CommandInputPage(self)
        case _:
            HandlePageNotFound(self)
        