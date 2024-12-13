from InquirerPy import inquirer
from rich.text import Text
from rich.console import Console
from rich.table import Table
from InquirerPy.base.control import Choice
from yaspin import yaspin

import json
import os
import time

from .utils import linebreak, generate_report, task_createdAt, clear_terminal, get_configuration, create_folder, get_projects, heading, get_json_file
from .styles import custom_syles
from .constants import themes, pointer_options, priority_options
from .task import Task

console = Console()

config_file = os.path.join('../taskscript_v2', '.config.json')
app_config = get_configuration()
storage_directory = os.path.join('./.storage')


def configure_application(title="configure application"):
    heading(title)

    project_directory = inquirer.filepath(
        message="Enter your project directory",
        default=app_config.get("project_directory", '.'),
        style=custom_syles,
    ).execute()

    theme = inquirer.select(
        message="Select theme",
        choices=themes,
        style=custom_syles,
        pointer=app_config['pointer'],
        default=app_config.get("theme", 'dark')
    ).execute()

    pointer = inquirer.select(
        message="Select pointer",
        choices=pointer_options,
        style=custom_syles,
        default=app_config.get("pointer", "▶"),
        pointer=app_config['pointer']
    ).execute()

    config_dict = {
        "project_directory": project_directory,
        "theme": theme,
        "pointer": pointer
    }

    linebreak()
    console.print(
        f"  [grey39]Project directory[/grey39]: {app_config['project_directory']}")
    console.print(f"  [grey39]Theme[/grey39]:  {app_config['theme']}")
    console.print(f"  [grey39]Pointer[/grey39]: {app_config['pointer']}")
    linebreak()

    confirm_save = inquirer.confirm(
        message='Confirm save changes to configuration file?',
        style=custom_syles,
        default=True
    ).execute()

    if confirm_save:
        with console.status('Setting configuration...') as st:
            with open(config_file, 'w') as f:
                f.write(json.dumps(config_dict, indent=4))
            time.sleep(0.2)
            st.update("✔ Successfully set configuration")

        main_menu()
    else:
        main_menu()


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

    if main_menu_choice == 2:
        view_configuration()

    if main_menu_choice == 3:
        update_configuration()

    if main_menu_choice == 4:
        view_reports()

    if main_menu_choice == 5:
        exit_application()


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
        folder_abs_path = os.path.abspath(
            os.path.join(storage_directory, new_project_title))
        file_path = os.path.join(
            storage_directory, new_project_title, f'_{new_project_title}_tasks.json')
        file_abs_path = os.path.abspath(file_path)

        with console.status("Creating folders..."):
            time.sleep(0.3)
            create_folder(new_project_title)
            console.print(
                f"[green]✔[/green] Successfully created [light_slate_blue][link=file:///{folder_abs_path}]{new_project_title}[/link][/light_slate_blue] and ready for tasks.\n[green]✔[/green] Successfully created [grey39][link=file:///{file_abs_path}]_{new_project_title}.json[/link][/grey39].")

    except FileExistsError:
        console.print(
            f"[red bold]x[/red bold] [light_slate_blue][link=file:///{folder_abs_path}]{folder}[/link][/light_slate_blue] already exists.")
    except PermissionError:
        console.print(
            f"[red bold]✗[/red bold] Permission denied: Unable to create '{new_project_title}'")
    except Exception as e:
        console.print(f"[red bold]✗[/red bold] An error occured: {e}")

    linebreak()

    options = [
        Choice(name='View all projects', value=0),
        Choice(name='Create new project', value=1),
        Choice(name='Back to main menu', value=2)
    ]

    selected_option = inquirer.select(
        message='Select option',
        pointer=app_config['pointer'],
        style=custom_syles,
        choices=options
    ).execute()

    if selected_option == 0:
        view_projects()
    if selected_option == 1:
        create_new_project()
    if selected_option == 2:
        main_menu()


# generate tasks for each project
def generate_tasks_for_projects():
    heading("Generate tasks")
    folders = os.listdir(app_config['project_directory'])

    available_folders = []

    available_folders = [Choice(f'{folder}', name=folder)
                         for folder in folders]

    selected_folders = inquirer.checkbox(
        message="Select folders to generate tasks for",
        instruction='Leave blank to go back',
        choices=available_folders,
        pointer=app_config['pointer']
    ).execute()

    if len(selected_folders) < 1:
        main_menu()
    else:
        linebreak()

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
                    print(
                        f"Permission denied: Unable to create '{folder}'")
                except Exception as e:
                    print(f"An error occured: {e}")

        options = [
            Choice(name='View all projects', value=0),
            Choice(name='Create new project', value=1),
            Choice(name='Back to main menu', value=2)
        ]
        linebreak()
        selected_option = inquirer.select(
            message='Select option',
            pointer=app_config['pointer'],
            style=custom_syles,
            choices=options
        ).execute()

        if selected_option == 0:
            view_projects()
        if selected_option == 1:
            create_new_project()
        if selected_option == 2:
            main_menu()

# view all projects


def view_projects():
    heading("View projects")

    projects = get_projects()

    fuzzy_projects = []

    if len(projects) < 1:
        console.print("  [bright_magenta]*You don't have any projects yet")

        options = [
            Choice(name='Create tasks from exisiting project', value=0),
            Choice(name='Create a new project', value=1),
            Choice(name='Back to main menu', value=3)
        ]

        linebreak()

        selected_option = inquirer.select(
            message='Select option',
            choices=options,
            pointer=app_config['pointer'],
            style=custom_syles
        ).execute()

        if selected_option == 0:
            generate_tasks_for_projects()
        if selected_option == 1:
            create_new_project()
        if selected_option == 3 or selected_option == None:
            main_menu()
    else:
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


def view_project_tasks(project, filter='', sort_option='', sort_order=''):
    clear_terminal()
    tasks = load_tasks(project)

    completed_tasks = [task for task in tasks if tasks[task]['isComplete']]

    filter_category = 'priority' if filter in [
        'high', 'normal', 'low'] else 'status' if filter in ['completed', 'pending'] else 'tag'

    arrow = '▲' if sort_order =='asc' else '▼'
    console.print(
        f"\n  [underline]{project}[/underline]{f' ∙ {filter_category} [grey39]|[/grey39] {filter}' if filter and not filter == 'all' else ''}{f' ∙ {arrow} {sort_option}' if not sort_option == '' else ''} ∙ [grey39][{len(completed_tasks)}/{len(tasks)}][/grey39]\n")

    state_tasks = tasks.items()

    def priority_sort(task):
        (task_id, task_details) = task

        return task_details['priority'] * -1 if sort_order == 'desc' else task_details['priority'] * 1

    if sort_option == 'priority':
        sorted_tasks = sorted(state_tasks, key=priority_sort)

        state_tasks = sorted_tasks

    for index, (task_id, task_details) in enumerate(state_tasks):
        if filter == 'all' or filter == '':
            render_task(task_details, index)
        if filter == 'completed':
            render_task(
                task_details, index) if task_details['isComplete'] else None
        if filter == 'pending':
            render_task(
                task_details, index) if not task_details['isComplete'] else None
        if filter == 'high':
            render_task(
                task_details, index) if not task_details['priority'] == 1 else None
        if filter == 'normal':
            render_task(
                task_details, index) if not task_details['priority'] == 2 else None
        if filter == 'low':
            render_task(
                task_details, index) if not task_details['priority'] == 3 else None
        if filter.startswith("@"):
            render_task(
                task_details, index) if filter[1:] in task_details['tags'] else None

    task_options = [
        Choice(name="Add task", value=0),
        Choice(name="Edit task", value=1),
        Choice(name="Select tasks", value=2),
        Choice(name="Filter tasks", value=3),
        Choice(name="Search tasks", value=4),
        Choice(name="Sort tasks", value=8),
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
        filter_categories = [
            Choice(name="Filter by Status", value="status"),
            Choice(name="Filter by Tags", value="tag"),
            Choice(name="Filter by Priority", value="priority"),
        ]

        status_filters = [
            Choice(value="all", name="All tasks"),
            Choice(value="completed", name="Completed tasks"),
            Choice(value="pending", name="Pending tasks"),
        ]

        priority_filters = [
            Choice(name='All tasks', value='all'),
            Choice(name="High", value='high'),
            Choice(name="Normal", value='normal'),
            Choice(name="Low", value='low')
        ]

        tags = []

        for (task_id, task_details) in tasks.items():
            for tag in task_details['tags']:
                tag_choice = Choice(name=f'@{tag}', value=f'@{tag}')
                tags.append(tag_choice)

        filter_option = inquirer.select(
            message='Filter by:',
            choices=filter_categories,
            pointer=app_config['pointer'],
            default='status'
        ).execute()

        if filter_option == 'status':

            status_filter = inquirer.select(
                message='Filter by status',
                choices=status_filters,
                pointer=app_config['pointer'],
                style=custom_syles,
                default='all'
            ).execute()

            view_project_tasks(project, status_filter)

        if filter_option == 'tag':

            tags_filter = inquirer.select(
                message='Filter by priority',
                choices=[Choice(name='All tasks', value='all')] + tags,
                pointer=app_config['pointer'],
                style=custom_syles,
                default='all'
            ).execute()

            view_project_tasks(project, tags_filter)

        if filter_option == 'priority':
            priority_filter = inquirer.select(
                message='Filter by priority',
                choices=priority_filters,
                pointer=app_config['pointer'],
                style=custom_syles,
                default='all'
            ).execute()

            view_project_tasks(project, priority_filter)

    if selected_option == 6:
        main_menu()

    if selected_option == 7:
        exit_application()

    if selected_option == 8:
        sorting_categories = [
            Choice(name='Sort by Date', value='date'),
            Choice(name='Sort by Priority', value='priority'),
        ]

        sorting_orders = [
            Choice(name='Ascending', value='asc'),
            Choice(name='Descending', value='desc')
        ]

        sorting_option = inquirer.select(
            message='Sort by',
            choices=sorting_categories,
            pointer=app_config['pointer'],
            style=custom_syles
        ).execute()

        sorting_order = inquirer.select(
            message='Select sorting order',
            choices=sorting_orders,
            pointer=app_config['pointer'],
            style=custom_syles
        ).execute()

        view_project_tasks(project, '', sorting_option, sorting_order)


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
        default='Normal',
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

    # add tags
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

    # change priority
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

    # mark as complete
    if select_action == 2:
        for index, (task_id, task_details) in enumerate(tasks.items()):
            if (index + 1) in selected_indices:
                task_details['isComplete'] = True

        with open(file_path, 'w') as f:
            json.dump(tasks, f)

        view_project_tasks(project)

    # mark as incomplete
    if select_action == 3:
        for index, (task_id, task_details) in enumerate(tasks.items()):
            if (index + 1) in selected_indices:
                task_details['isComplete'] = False

        with open(file_path, 'w') as f:
            json.dump(tasks, f)

        view_project_tasks(project)

    # delete tasks
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
    status = '[chartreuse1]✔[/chartreuse1]' if isComplete else "□"
    description = f"[grey39]{details['description']}[/grey39]" if isComplete else f"{details['description']}"

    priorities = ['[cornflower_blue]∙[/cornflower_blue]',
                  '[green3]∙[/green3]', '[red3]∙[/red3]']

    console.print(
        f"  [yellow]{'★' if details['isStarred'] else ' '} [/yellow][grey30]{index + 1}.[/grey30] {status} {description} [grey39]{task_createdAt(details['_timestamp'])}[/grey39] [yellow]{' '.join([f'@{tag.strip()} ' for tag in details['tags'] if tag.strip()])}[/yellow]{priorities[details['priority']]}")

    # load tasks from json file


def load_tasks(project):

    json_path = get_json_file(project)
    with open(json_path, 'r') as file:
        data = json.load(file)

    return data


def view_configuration():
    heading("App configuration")

    console.print(
        f"  [grey46]Project directory[/grey46]: {app_config['project_directory']}")
    console.print(f"  [grey46]Theme[/grey46]:  {app_config['theme']}")
    console.print(f"  [grey46]Pointer[/grey46]: {app_config['pointer']}")

    options = [
        Choice(name="Update configuration", value=0),
        Choice(name="Back to main menu", value=1),
    ]

    linebreak()

    selected_option = inquirer.select(
        message='Select option',
        style=custom_syles,
        pointer=app_config['pointer'],
        choices=options,
        default=1
    ).execute()

    if selected_option == 0:
        update_configuration()
    if selected_option == 1:
        main_menu()

# update the configuration


def update_configuration():
    configure_application(title='Update configuration')


def view_reports():

    heading("Reports")

    projects = get_projects()

    if len(projects) < 1:
        console.print("  [bright_magenta]*You don't have any projects yet")
        options = [
            Choice(name='Create tasks from exisiting project', value=0),
            Choice(name='Create a new project', value=1),
            Choice(name='Back to main menu', value=3)
        ]

        linebreak()

        selected_option = inquirer.select(
            message='Select option',
            choices=options,
            pointer=app_config['pointer'],
            style=custom_syles
        ).execute()

        if selected_option == 0:
            generate_tasks_for_projects()
        if selected_option == 1:
            create_new_project()
        if selected_option == 3 or selected_option == None:
            main_menu()

    else:
        reports_table = Table(title='Tasks')

        data = []

        reports_table.add_column("#", justify="center", style="bright_cyan")
        reports_table.add_column("Folder", justify="left", style="#e5c07b")
        reports_table.add_column("Progress", justify="left", style="#e5c07b")

        for (project_index, project) in enumerate(projects):
            completed_tasks = 0
            pending_tasks = 0
            total_tasks = 0

            for (index, (task_id, task_details)) in enumerate(load_tasks(project).items()):
                total_tasks += 1
                if task_details['isComplete'] == True:
                    completed_tasks += 1
                else:
                    pending_tasks += 1

            percentage_complete = round(
                (completed_tasks/total_tasks)*100) if total_tasks > 0 else 0
            bars = int(percentage_complete / 10) if total_tasks > 0 else 0
            strokes = 10 - bars

            graph = f"[{'[white]█[/white]'*bars}{'-'*strokes}]"

            stats = f"{graph} {percentage_complete}% ({completed_tasks}/{total_tasks})"

            data.append({
                'id': project_index + 1,
                'project': project,
                'completed_tasks': completed_tasks,
                'pending_tasks': pending_tasks,
                'total_tasks': total_tasks
            })

            reports_table.add_row(str(project_index + 1), project, stats)

        console.print(reports_table)

        report_options = [
            Choice(name='Export reports', value=0),
            Choice(name='Back to main menu', value=1)
        ]

        linebreak()

        selected_report_option = inquirer.select(
            message='Select option',
            choices=report_options,
            pointer=app_config['pointer'],
            style=custom_syles
        ).execute()

        if selected_report_option == 0:
            format_options = [
                Choice(name='CSV', value='csv'),
                Choice(name='JSON', value='json'),
                Choice(name='HTML', value='html'),
                Choice(name='SVG', value='svg'),
            ]

            selected_formats = inquirer.select(
                message='Select format',
                style=custom_syles,
                choices=format_options,
                multiselect=True

            ).execute()

            generate_report(selected_formats, reports_table, data)

            linebreak()

            next_steps = [
                Choice(name='Back to main menu', value=0)
            ]

            next_step = inquirer.select(
                message='Select option',
                choices=next_steps,
                pointer=app_config['pointer'],
                style=custom_syles
            ).execute()

            main_menu()

        if selected_report_option == 1:
            main_menu()


def exit_application():
    heading("Exited application")
    exit
