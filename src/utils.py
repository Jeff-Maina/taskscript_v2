import os
import json

from rich.console import Console
console = Console(record=True)


config_file = os.path.join('../taskscript_v2', '.config.json')
storage_directory = os.path.join('./.storage')


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


def get_json_file(project):
    return os.path.join(storage_directory, project,
                        f'_{project}-todos.json')


# generate_reports

def generate_report(selected_formats, table, reports_data):

    if 'html' in selected_formats or 'svg' in selected_formats or 'txt' in selected_formats:
        console.print(table)

    reports_folder = 'reports'
    os.makedirs(reports_folder, exist_ok=True)

    for format in selected_formats:

        if format == 'html':
            html_file = 'reports_table.html'

            html = console.export_html(clear=False)

            with open(os.path.join(reports_folder, html_file), 'w') as file:
                file.write(html)

        if format == 'svg':
            svg_file = 'reports_table.svg'

            svg = console.export_svg(clear=False)

            with open(os.path.join(reports_folder, svg_file), 'w') as file:
                file.write(svg)

        if format == 'csv':

            cols = 'Index,Folder,Completed tasks,Pending tasks,Total tasks'

            with open(os.path.join(reports_folder, 'reports.csv'), 'w') as file:
                file.write(f"{cols}\n")
                for data in reports_data:
                    file.write(
                        f"{data['id']},{data['project']},{data['completed_tasks']},{data['pending_tasks']},{data['total_tasks']}\n")


        if format == 'json':
            with open(os.path.join(reports_folder, 'reports.json'), 'w') as file:
                file.write("[\n")
                for index, data in enumerate(reports_data):
                    if index == len(reports_data) - 1:
                        file.write(f"{json.dumps(data)}\n")
                    else:
                        file.write(f"{json.dumps(data)},\n")
                file.write("]\n")