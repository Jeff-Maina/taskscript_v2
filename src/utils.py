import os
import json

from rich.console import Console
console = Console()


config_file = os.path.join('../taskscript_v2', '.config.json')
storage_directory = os.path.join('../taskscript_v2', '.storage')

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def linebreak(separator=" "):
    print(separator * 30)


def has_configured():
    return True if os.path.exists(".config.json") else False


def get_configuration():
    with open(config_file, 'r') as f:
        return json.load(f)


def create_folder(folder):
    app_config = get_configuration()

    if not os.path.exists(folder):
        folder_path = os.path.join(storage_directory, folder)

        os.makedirs(folder_path)
        folder_abs_path = os.path.abspath(folder_path)
        console.print(
            f"[green]✔[/green] Succesfully created [light_slate_blue][link=file:///{folder_abs_path}]{folder}[/link][/light_slate_blue]")

        file_name = f'{folder}_todos.json'
        file_path = os.path.join(storage_directory, folder, file_name)

        file_abs_path = os.path.abspath(file_path)
        with open(file_path, 'w') as f:
            f.write("{\n}")

            console.print(
                f"[green]✔[/green] Succesfully created [grey39][link=file:///{file_abs_path}]{file_name}[/link][/grey39]")
    else:
        console.print(
                f"[red]✔[/red][grey39][link=file:///{file_path}]{folder}[/link][/grey39] already exists.")
