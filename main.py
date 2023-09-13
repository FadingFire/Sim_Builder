import sys
import os

from python.src.main.server import run


current_file = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file))
sys.path.insert(0, project_root)
if __name__ == "__main__":
    run()
