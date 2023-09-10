from endpoint.post_endpoints.command_line import HandleCommand

from endpoint.get_endpoints.command_input import CommandInputPage

from endpoint.error_endpoints.page_not_found import HandlePageNotFound


def SendToCorrectEndpointsGet(self):
    match self.path:
        case '/commandline':
            HandleCommand(self)
        case '/':
            CommandInputPage(self)
        case _:
            HandlePageNotFound(self)
        