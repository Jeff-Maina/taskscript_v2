import os
import json

from rich.console import Console
console = Console()


config_file = os.path.join('../taskscript_v2', '.config.json')
storage_directory = './.storage'

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# markup
def linebreak(separator=" "):
    print(separator * 30)

def heading(title):
    clear_terminal()
    console.print(f"\n  [red bold]{title}\n")

def has_configured():
    return True if os.path.exists(".config.json") else False


def get_configuration():
    with open(config_file, 'r') as f:
        return json.load(f)


def create_folder(folder):
    folder_path = os.path.join(storage_directory, folder)

    if not os.path.exists(folder_path):

        os.makedirs(folder_path)
        
        file_name = f'_{folder}-todos.json'
        file_path = os.path.join(storage_directory, folder, file_name)
        
        with open(file_path, 'w') as f:
            f.write("{\n}")
    else:
        raise FileExistsError

def get_projects():
    folders = os.listdir(storage_directory)

    return folders