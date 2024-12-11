import os
import json

config_file = os.path.join('../taskscript_v2', '.config.json')

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def linebreak(separator=" "):
    print( separator * 30 )

def has_configured():
    return True if os.path.exists(".config.json") else False


def get_configuration():
    with open(config_file, 'r') as f:
        return json.load(f)
