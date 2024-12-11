from InquirerPy import inquirer
from rich.console import Console

import json
import os

from .utils import linebreak, clear_terminal, get_configuration
from .styles import custom_syles
from .constants import themes, pointer_options

console = Console()
config_file = os.path.join('../taskscript_v2', '.config.json')
app_config = get_configuration()


def configure_application():
    console.print("  configure application")
    linebreak()

    project_directory = inquirer.filepath(
        message="Enter your project directory",
        default=".",
        style=custom_syles,
    ).execute()

    theme = inquirer.select(
        message="Select theme",
        choices=themes,
        style=custom_syles,
        pointer=app_config['pointer']
    ).execute()

    pointer = inquirer.select(
        message="Select pointer",
        choices=pointer_options,
        style=custom_syles,
        pointer=app_config['pointer']
    ).execute()

    config_dict = {
        "project_directory": project_directory,
        "theme": theme,
        "pointer": pointer
    }

    with open(config_file, 'w') as f:
        f.write(json.dumps(config_dict, indent=4))


def main_menu():
    pass
