import os
import json
import time
import datetime

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

        linebreak()

    reports_folder = 'reports'
    os.makedirs(reports_folder, exist_ok=True)

    with console.status("Generating reports...") as st:
        for format in selected_formats:

            if format == 'html':
                html_file = 'reports_table.html'

                html = console.export_html(clear=False)
               
                with open(os.path.join(reports_folder, html_file), 'w') as file:
                    file.write(html)

                    console.print(
                        f"[green]✔[/green] Successfully created [light_slate_blue][link=file:///{os.path.abspath(os.path.join(reports_folder, html_file))}]{html_file}[/link][/light_slate_blue]")
                    time.sleep(0.2)

            if format == 'svg':
                svg_file = 'reports_table.svg'

                svg = console.export_svg(clear=False)

                with open(os.path.join(reports_folder, svg_file), 'w') as file:
                    file.write(svg)

                    console.print(
                        f"[green]✔[/green] Successfully created [light_slate_blue][link=file:///{os.path.abspath(os.path.join(reports_folder, svg_file))}]{svg_file}[/link][/light_slate_blue]")
                    time.sleep(0.2)

            if format == 'csv':

                cols = 'Index,Folder,Completed tasks,Pending tasks,Total tasks'

                with open(os.path.join(reports_folder, 'reports.csv'), 'w') as file:
                    file.write(f"{cols}\n")
                    for data in reports_data:
                        file.write(
                            f"{data['id']},{data['project']},{data['completed_tasks']},{data['pending_tasks']},{data['total_tasks']}\n")

                    console.print(
                        f"[green]✔[/green] Successfully created [light_slate_blue][link=file:///{os.path.abspath(os.path.join(reports_folder, 'reports.csv'))}]reports.csv[/link][/light_slate_blue]")
                    time.sleep(0.2)

            if format == 'json':
                with open(os.path.join(reports_folder, 'reports.json'), 'w') as file:
                    file.write("[\n")
                    for index, data in enumerate(reports_data):
                        if index == len(reports_data) - 1:
                            file.write(f"{json.dumps(data)}\n")
                        else:
                            file.write(f"{json.dumps(data)},\n")
                    file.write("]\n")

                    console.print(
                        f"[green]✔[/green] Successfully created [light_slate_blue][link=file:///{os.path.abspath(os.path.join(reports_folder, 'reports.json'))}]reports.json[/link][/light_slate_blue]")
                    time.sleep(0.2)


def task_createdAt(timestamp):
    now = datetime.datetime.now()
    target_time = datetime.datetime.fromtimestamp(timestamp)
    delta = now - target_time

    total_seconds = int(delta.total_seconds())

    days = total_seconds // 86400  
    hours = (total_seconds % 86400) // 3600  
    minutes = (total_seconds % 3600) // 60

    if total_seconds < 60:
        return f"{total_seconds}s"
    
    if total_seconds < 3600:
        return f"{minutes}m"
    
    if total_seconds < 86400:
        return f"{hours}h"

    return f"{days}d"