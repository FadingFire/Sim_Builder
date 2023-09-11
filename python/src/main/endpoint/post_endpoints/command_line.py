from http.server import SimpleHTTPRequestHandler
from model.paths import post_response_page

# TODO: a thing you could want tot write is some code that uses the bluesky api to validate the responses though i dont if they have that programmed in.



def HandleCommand(self):   # TODO: remember to talk to me about how you want to return a succes message etc
    command = parseCommand(self)
    if(command[0] != 200):
        return 505
    useCommand(command[1])
    self.path = post_response_page()
    return SimpleHTTPRequestHandler.do_GET(self)


def parseCommand(self):
    content_length = int(self.headers['Content-Length'])
    post_data = self.rfile.read(content_length).decode('utf-8')
    for i, char in enumerate(post_data):
        if(char == "="):
            break
    validatedData = validataRawPostData(post_data)
    if(validatedData[0] != 200):
        return 505
    
    command = post_data[validatedData[1]:len(post_data)]
    print(command)
    
    # TODO: this does work its just that some char still get converted becacause you cant have spaces inside of stuff etc 
    
    if(validateCommand(self, command) != 200):
        return 505
    return 200, command


def validataRawPostData(postData):
    for i, char in enumerate(postData):
        if(char == "=" and i+1 <= len(postData) ):   # FIXME: this might actualy be the other way around instead of <= maybe its >= idk im stupid and not testing it
            return 200, i+1
    return 404, 0


def validateCommand(self, command):     # TODO: check if the parsed data is a command that either the user can do or if the command actualy exist
    return 200


def useCommand(command):     # TODO: this is going to be the painfull procces The command to the plugin
    print(command)
    return