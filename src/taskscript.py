from InquirerPy import inquirer
from rich.console import Console
from InquirerPy.base.control import Choice

import json
import os
import time

from .utils import linebreak, clear_terminal, get_configuration, create_folder
from .styles import custom_syles
from .constants import themes, pointer_options

console = Console()
config_file = os.path.join('../taskscript_v2', '.config.json')
app_config = get_configuration()
storage_directory = os.path.join('../taskscript_v2', '.storage')


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
    clear_terminal()

    console.print("\n[red bold] Main menu\n")

    main_menu_options = [
        Choice(name="Generate tasks for projects", value=0),
        Choice(name="View projects", value=1),
        Choice(name="View current configuration", value=2),
        Choice(name="Update configuration", value=3),
        Choice(name="View Reports", value=4),
        Choice(name="Exit application", value=5),]

    main_menu_choice = inquirer.select(
        message="Select an option",
        choices=main_menu_options,
        style=custom_syles,
        pointer=app_config['pointer']
    ).execute()

    if main_menu_choice == 0:
        manage_project_tasks()

    if main_menu_choice == 1:
        view_projects()


def manage_project_tasks():

    generate_options = [
        Choice(name='Generate tasks for existing projects', value=0),
        Choice(name='Create new project', value=1),
        Choice(name='Go back to main menu', value=2)
    ]
    generate_options_choice = inquirer.select(
        message='Select an option',
        choices=generate_options,
        style=custom_syles,
        pointer=app_config['pointer']
    ).execute()

    if generate_options_choice == 0:
        generate_tasks_for_projects()
    if generate_options_choice == 1:
        new_project_title = inquirer.text(
            message='Enter title for new project',
            style=custom_syles,
        ).execute()
        linebreak()
        create_folder(new_project_title)
        linebreak()

    proceed_options = [
        Choice(name='View projects', value=0),
        Choice(name='Go back to main menu', value=1),
        Choice(name='Exit application', value=2)
    ]

    proceed_options_choice = inquirer.select(
        message='Select an option',
        choices=proceed_options,
        style=custom_syles,
        pointer=app_config['pointer']
    ).execute()

    if proceed_options_choice == 0:
        view_projects()
    if proceed_options_choice == 1:
        main_menu()
    if proceed_options_choice == 2:
        exit_application()


def generate_tasks_for_projects():
    clear_terminal()
    console.print("\n  [red bold]Generate tasks\n")

    folders = os.listdir(app_config['project_directory'])

    selected_folders = inquirer.checkbox(
        message="Select folders to generate tasks for",
        choices=folders,
        style=custom_syles,
        pointer=app_config['pointer']
    ).execute()

    linebreak()
    with console.status("[magenta]Generating tasks...") as status:
        for folder in selected_folders:
            folder_path = os.path.join(storage_directory, folder)
            folder_abs_path = os.path.abspath(folder_path)
            try:
                time.sleep(0.3)
                create_folder(folder)
            except FileExistsError:
                console.print(
                    f"[red]☐[/red] [light_slate_blue][link=file:///{folder_abs_path}]{folder}[/link][/light_slate_blue] already exists.")
            except PermissionError:
                print(f"Permission denied: Unable to create '{folder}'")
            except Exception as e:
                print(f"An error occured: {e}")


def view_projects():
    pass


def view_configuration():
    pass


def update_configuration():
    pass


def view_reports():
    pass


def exit_application():
    clear_terminal()
    linebreak()
    console.print("Goodbye!")
    linebreak()
