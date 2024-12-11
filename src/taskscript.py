from InquirerPy import inquirer
from rich.text import Text
from rich.console import Console
from InquirerPy.base.control import Choice
from yaspin import yaspin

import json
import os
import time

from .utils import linebreak, clear_terminal, get_configuration, create_folder, get_projects, heading
from .styles import custom_syles
from .constants import themes, pointer_options, priority_options
from .task import Task

console = Console()

config_file = os.path.join('../taskscript_v2', '.config.json')
app_config = get_configuration()
storage_directory = os.path.join('./.storage')


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

    heading("Project task management")

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
        create_new_project()

    proceed_options = [
        Choice(name='View projects', value=0),
        Choice(name='Add another project', value=3),
        Choice(name='Go back to main menu', value=1),
        Choice(name='Exit application', value=2)
    ]

    linebreak()

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
    if proceed_options_choice == 3:
        create_new_project()


def create_new_project():
    heading('Create new project')

    new_project_title = inquirer.text(
        message='Enter title for new project',
        style=custom_syles,
    ).execute()
    linebreak()

    # get the absolute path of the new folder
    folder_path = os.path.join(storage_directory, new_project_title)
    folder_abs_path = os.path.abspath(folder_path)

    try:
        with console.status("[magenta]Generating tasks...") as status:
            time.sleep(0.3)
            create_folder(new_project_title)
    except FileExistsError:
        console.print(
            f"[red bold]✗[/red bold] [light_slate_blue][link=file:///{folder_abs_path}]{new_project_title}[/link][/light_slate_blue] already exists.")
    except PermissionError:
        console.print(
            f"[red bold]✗[/red bold] Permission denied: Unable to create '{new_project_title}'")
    except Exception as e:
        console.print(f"[red bold]✗[/red bold] An error occured: {e}")

    linebreak()


# generate tasks for each project
def generate_tasks_for_projects():
    heading("Generate tasks")
    folders = os.listdir(app_config['project_directory'])

    available_folders = []

    available_folders = [Choice(f'{folder}', name=folder)
                         for folder in folders]

    selected_folders = inquirer.checkbox(
        message="Select folders to generate tasks for",
        choices=available_folders,
        pointer=app_config['pointer']
    ).execute()

    linebreak()

    if len(selected_folders) > 0:
        with console.status("Creating folders..."):
            for folder in selected_folders:

                folder_abs_path = os.path.abspath(
                    os.path.join(storage_directory, folder))
                file_path = os.path.join(
                    storage_directory, folder, f'_{folder}_tasks.json')
                file_abs_path = os.path.abspath(file_path)

                try:
                    time.sleep(0.3)
                    create_folder(folder)
                    console.print(
                        f"[green]✔[/green] Successfully created [light_slate_blue][link=file:///{folder_abs_path}]{folder}[/link][/light_slate_blue] and ready for tasks.\n[green]✔[/green] Successfully created [grey39][link=file:///{file_abs_path}]_{folder}.json[/link][/grey39].")
                except FileExistsError:
                    console.print(
                        f"[red bold]x[/red bold] [light_slate_blue][link=file:///{folder_abs_path}]{folder}[/link][/light_slate_blue] already exists.")
                except PermissionError:
                    print(f"Permission denied: Unable to create '{folder}'")
                except Exception as e:
                    print(f"An error occured: {e}")

# view all projects


def view_projects():
    heading("View projects")

    projects = get_projects()

    fuzzy_projects = []

    for (index, project) in enumerate(projects):
        project_choice = Choice(name=project, value=project)
        fuzzy_projects.append(project_choice)

    selected_project = inquirer.fuzzy(
        message='Select project',
        choices=fuzzy_projects + ['◀ Back to main menu'],
        style=custom_syles,
        pointer=app_config['pointer'],
        match_exact=True
    ).execute()

    if selected_project == '◀ Back to main menu':
        main_menu()
    else:
        view_project_tasks(selected_project)


def view_project_tasks(project):
    clear_terminal()
    tasks = load_tasks(project)

    completed_tasks = [task for task in tasks if tasks[task]['isComplete']]

    console.print(
        f"\n  [underline]{project}[/underline]  [grey39][{len(completed_tasks)}/{len(tasks)}][/grey39]\n")

    for task_id, task_details in tasks.items():
        isComplete = task_details['isComplete']
        status = '✔' if isComplete else "□"
        description = f"[grey39]{task_details['description']}[/grey39]" if isComplete else f"{task_details['description']}"

        console.print(
            f"  {task_details['_id']}. {status} {description} [yellow]{','.join(task_details['tags'])}[/yellow]")

    task_options = [
        Choice(name="Add task", value=0),
        Choice(name="Edit task", value=1),
        Choice(name="Select tasks", value=2),
        Choice(name="Filter tasks", value=3),
        Choice(name="Search tasks", value=4),
        Choice(name="Export/Import tasks", value=5),
        Choice(name="Go back to main menu", value=6),
        Choice(name="Exit application", value=7)
    ]

    linebreak()

    selected_option = inquirer.select(
        message="Select an option",
        choices=task_options,
        pointer=app_config['pointer'],
        style=custom_syles
    ).execute()

    if selected_option == 0:
        add_task(project, tasks)

        view_project_tasks(project)

    if selected_option == 6:
        main_menu()

    if selected_option == 7:
        exit_application()


def add_task(project, tasks):

    task_description = inquirer.text(
        message="Enter task description",
        style=custom_syles,
    ).execute()

    task_tags = inquirer.text(
        message="Enter task tags (comma-separated)",
        style=custom_syles,
    ).execute()

    priority = inquirer.select(
        message="Select task priority",
        choices=priority_options,
        style=custom_syles,
        default='Medium',
        pointer=app_config['pointer']
    ).execute()

    task_tags = [f'@{tag.strip()}' for tag in task_tags.split(',') if tag.strip()]

    task = Task(len(tasks) + 1, task_description, priority, task_tags)

    tasks[task._id] = task.to_json()

    json_path = os.path.join(storage_directory, project,
                             f'_{project}-todos.json')

    with open(json_path, 'w') as file:
        json.dump(tasks, file)

# load tasks from json file


def load_tasks(project):
    json_path = os.path.join(storage_directory, project,
                             f'_{project}-todos.json')

    with open(json_path, 'r') as file:
        data = json.load(file)

    return data


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
