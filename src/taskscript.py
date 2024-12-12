from InquirerPy import inquirer
from rich.text import Text
from rich.console import Console
from InquirerPy.base.control import Choice
from yaspin import yaspin

import json
import os
import time

from .utils import linebreak, clear_terminal, get_configuration, create_folder, get_projects, heading, get_json_file
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

    for index, (task_id, task_details) in enumerate(tasks.items()):
        render_task(task_details, index)
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

    if selected_option == 1:
        edit_task(project, tasks)

        view_project_tasks(project)

    if selected_option == 2:
        selected_tasks = inquirer.text(
            message="Enter task tags (comma-separated)",
            style=custom_syles,
        ).execute()

        selected_indices = [int(task.strip())
                            for task in selected_tasks.split(",") if task.strip()]

        select_tasks(project, tasks, selected_indices)
    if selected_option == 3:
        pass
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

    task_tags = [
        f'@{tag.strip()}' for tag in task_tags.split(',') if tag.strip()]

    task = Task(len(tasks) + 1, task_description, priority, task_tags)

    tasks[task._id] = task.to_json()

    json_path = get_json_file(project)

    with open(json_path, 'w') as file:
        json.dump(tasks, file)


def edit_task(project, tasks):

    selected_task = inquirer.number(
        message='Enter the task index',
        style=custom_syles,
        min_allowed=1,
        max_allowed=len(tasks)
    ).execute()

    task = tasks[selected_task]

    new_title = inquirer.text(
        message="Enter new task description",
        style=custom_syles,
        default=task['description']
    ).execute()

    tags = inquirer.text(
        message='Enter tags',
        default=",".join(task['tags']),
        style=custom_syles
    ).execute()

    priority = inquirer.select(
        message='Enter new priority',
        default=task['priority'],
        style=custom_syles,
        choices=priority_options
    ).execute()

    task['title'] = new_title
    task['tags'] = tags.split(",")
    task['priority'] = priority

    file_path = get_json_file(project)

    with open(file_path, 'w') as f:
        json.dump(tasks, f)


def delete_task(project, tasks, selected_indices):
    pass


def select_tasks(project, tasks, selected_indices):
    heading(f"Selected tasks [grey39]{len(selected_indices)} selected")

    file_path = get_json_file(project)

    for index, (task_id, task_details) in enumerate(tasks.items()):
        if (index + 1) in selected_indices:
            render_task(task_details, index)

    action_options = [
        Choice(name='Add tags', value=0),
        Choice(name='Change priority', value=1),
        Choice(name='Mark as complete', value=2),
        Choice(name='Mark as incomplete', value=3),
        Choice(name='Delete tasks', value=4),
        Choice(name='Back to tasklist', value=5),
    ]

    linebreak()
    select_action = inquirer.select(
        message='Select action',
        choices=action_options,
        style=custom_syles,
        pointer=app_config['pointer']
    ).execute()

    if select_action == 0:
        task_tags = inquirer.text(
            message="Enter task tags (comma-separated)",
            style=custom_syles,
        ).execute()

        task_tags = [
            f'@{tag.strip()}' for tag in task_tags.split(',') if tag.strip()]

        for index, (task_id, task_details) in enumerate(tasks.items()):
            if (index + 1) in selected_indices:
                task_details['tags'] = task_tags

        with open(file_path, 'w') as f:
            json.dump(tasks, f)

        view_project_tasks(project)

    if select_action == 1:
        priority = inquirer.select(
            message="Select priority",
            choices=priority_options,
            style=custom_syles,
            default='Medium',
            pointer=app_config['pointer']
        ).execute()

        for index, (task_id, task_details) in enumerate(tasks.items()):
            if (index + 1) in selected_indices:
                task_details['priority'] = priority

        view_project_tasks(project)

    if select_action == 2:
        for index, (task_id, task_details) in enumerate(tasks.items()):
            if (index + 1) in selected_indices:
                task_details['isComplete'] = True

    if select_action == 3:
        for index, (task_id, task_details) in enumerate(tasks.items()):
            if (index + 1) in selected_indices:
                task_details['isComplete'] = False

    if select_action == 4:

        filtered_tasks = {task_id: task_details for index, (task_id, task_details) in enumerate(
            tasks.items()) if (index + 1) not in selected_indices}

        with open(file_path, 'w') as f:
            json.dump(filtered_tasks, f)

        view_project_tasks(project)

    if select_action == 5:
        view_project_tasks(project)


def render_task(details, index):
    isComplete = details['isComplete']
    status = '✔' if isComplete else "□"
    description = f"[grey39]{details['description']}[/grey39]" if isComplete else f"{details['description']}"

    console.print(
        f"  {index + 1}. {status} {description} [yellow]{' '.join(details['tags'])}[/yellow]")

    # load tasks from json file


def load_tasks(project):
    
    json_path = get_json_file(project)
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
