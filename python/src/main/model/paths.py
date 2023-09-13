import os
import inspect

def get_page_path(filename):
    script_path = inspect.stack()[1][1]

    script_dir = os.path.dirname(os.path.abspath(script_path))
    static_file_dir = os.path.join(script_dir, 'python', 'src', 'main', 'pages')

    relative_path = os.path.relpath(os.path.join(static_file_dir, filename+".html"), script_dir)
    return relative_path