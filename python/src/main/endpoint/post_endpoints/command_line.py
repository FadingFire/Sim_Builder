from http.server import SimpleHTTPRequestHandler
from model.paths import index_page_path

def HandleCommand(self):
    # TODO: remember to talk to me about how you want to return a succes message etc
    ProccesCommand(self)
    return SimpleHTTPRequestHandler.do_GET(self)


def ProccesCommand(self):
    # TODO: this is going to be the painfull procces The command to the plugin
    status = 200
    print(status)
    return status