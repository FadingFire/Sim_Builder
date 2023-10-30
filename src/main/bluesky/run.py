import sys
from bluesky.__main__ import main
from src.main.flaskr.terminal.endpoint.terminal_endpoint import parse_command

def stop():
    print("text")

def start():
    sys.exit(main())
start()