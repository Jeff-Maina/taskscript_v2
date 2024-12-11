from InquirerPy import inquirer
from rich.console import Console
from InquirerPy.base.control import Choice

from src.taskscript import configure_application,main_menu

from src.utils import clear_terminal,has_configured,linebreak

console = Console()


def main():

    clear_terminal()

    linebreak()

    if has_configured():
        main_menu()
    else:
        configure_application()

    

    


if __name__== "__main__":
    main()
